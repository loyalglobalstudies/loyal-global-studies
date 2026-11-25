(function () {
  "use strict";

  if (window.LoyalVideoPlayer) return;

  const VIDEO_ID = /^[a-zA-Z0-9_-]{11}$/;

  function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }

  function validTeachers(teachers) {
    return (Array.isArray(teachers) ? teachers : [])
      .map((teacher, ti) => ({
        id: String(teacher.id || "teacher-" + ti),
        name: String(teacher.name || "Teacher"),
        lectures: (Array.isArray(teacher.lectures) ? teacher.lectures : [])
          .filter(lecture => lecture && VIDEO_ID.test(String(lecture.id || "")))
          .map((lecture, li) => ({
            id: String(lecture.id),
            title: String(lecture.title || "Lecture " + (li + 1))
          }))
      }))
      .filter(teacher => teacher.lectures.length);
  }

  function mount(options) {
    options = options || {};
    const root = typeof options.root === "string"
      ? document.querySelector(options.root)
      : options.root;

    if (!root) {
      console.error("LoyalVideoPlayer: player root not found.");
      return null;
    }

    const teachers = validTeachers(options.teachers);
    if (!teachers.length) {
      teachers.push({
        id: "classroom",
        name: "Classes coming soon",
        lectures: []
      });
    }

    root.hidden = false;
    root.replaceChildren();

    const storageKey = String(options.storageKey || "loyal_video_progress_v1");
    let activeTeacher = 0;
    let activeLecture = 0;
    let searchText = "";
    let completed = {};
    let last = {};

    try {
      const saved = JSON.parse(localStorage.getItem(storageKey) || "{}");
      completed = saved.completed || {};
      last = saved.last || {};
    } catch (_) {}

    const overlay = el("div", "lvp-overlay");
    overlay.hidden = true;

    const dialog = el("section", "lvp-dialog");
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-label", "Video classroom");

    const top = el("header", "lvp-top");
    const title = el("strong", "lvp-brand", options.title || "LOYAL Video Classroom");
    const close = el("button", "lvp-close", "✕");
    close.type = "button";
    close.setAttribute("aria-label", "Close player");
    top.append(title, close);

    const layout = el("div", "lvp-layout");
    const side = el("aside", "lvp-sidebar");
    const search = el("input", "lvp-search");
    search.type = "search";
    search.placeholder = "Search teacher or lecture…";
    search.setAttribute("aria-label", "Search lectures");

    const folderList = el("div", "lvp-folders");
    const lectureList = el("div", "lvp-lectures");
    side.append(search, folderList, lectureList);

    const main = el("main", "lvp-main");
    const now = el("div", "lvp-now", "Select a lecture");
    const videoBox = el("div", "lvp-video");
    const placeholder = el("div", "lvp-placeholder", "Lecture select करें");
    videoBox.append(placeholder);

    const controls = el("div", "lvp-controls");
    const prev = el("button", "", "← Previous");
    const next = el("button", "", "Next →");
    const done = el("button", "", "✓ Complete");
    const full = el("button", "", "⛶ Fullscreen");
    controls.append(prev, next, done, full);

    const status = el("div", "lvp-status", "");
    main.append(now, videoBox, controls, status);
    layout.append(side, main);
    dialog.append(top, layout);
    overlay.append(dialog);
    const launcher = el(
      "button",
      "lvp-launch",
      String(options.launchLabel || "▶ Open Video Classroom")
    );
    launcher.type = "button";
    launcher.addEventListener("click", open);

    root.append(launcher, overlay);

    function save() {
      try {
        localStorage.setItem(storageKey, JSON.stringify({
          completed,
          last: {
            teacher: activeTeacher,
            lecture: activeLecture
          }
        }));
      } catch (_) {}
    }

    function current() {
      return teachers[activeTeacher].lectures[activeLecture];
    }

    function showVideo() {
      const lecture = current();

      if (!lecture) {
        videoBox.replaceChildren(
          el("div", "lvp-placeholder", "Verified classes will be added here.")
        );
        now.textContent = "LOYAL Classroom";
        status.textContent = "इस बैच की कक्षाएँ जल्द उपलब्ध होंगी।";
        prev.disabled = true;
        next.disabled = true;
        done.disabled = true;
        full.disabled = true;
        return;
      }

      prev.disabled = false;
      next.disabled = false;
      done.disabled = false;
      full.disabled = false;
      videoBox.replaceChildren();
      const frame = el("iframe", "lvp-frame");
      frame.src = "https://www.youtube-nocookie.com/embed/" +
        encodeURIComponent(lecture.id) +
        "?rel=0&modestbranding=1";
      frame.title = lecture.title;
      frame.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
      frame.allowFullscreen = true;
      frame.loading = "lazy";
      videoBox.append(frame);

      now.textContent = teachers[activeTeacher].name + " · " + lecture.title;
      status.textContent = completed[lecture.id] ? "Completed ✓" : "Now playing";
      prev.disabled = activeLecture <= 0;
      next.disabled = activeLecture >= teachers[activeTeacher].lectures.length - 1;
      save();
      renderLectures();
    }

    function renderFolders() {
      folderList.replaceChildren();
      teachers.forEach((teacher, index) => {
        const button = el("button", "lvp-folder",
          teacher.name + " (" + teacher.lectures.length + ")");
        button.type = "button";
        button.setAttribute("aria-pressed", String(index === activeTeacher));
        button.addEventListener("click", () => {
          activeTeacher = index;
          activeLecture = 0;
          renderFolders();
          renderLectures();
          showVideo();
        });
        folderList.append(button);
      });
    }

    function renderLectures() {
      lectureList.replaceChildren();
      const teacher = teachers[activeTeacher];
      teacher.lectures.forEach((lecture, index) => {
        const haystack = (teacher.name + " " + lecture.title).toLowerCase();
        if (searchText && !haystack.includes(searchText)) return;

        const button = el("button", "lvp-lecture");
        button.type = "button";
        button.setAttribute("aria-current", String(index === activeLecture));
        const label = el("span", "", lecture.title);
        const mark = el("small", "", completed[lecture.id] ? "✓ Done" : "");
        button.append(label, mark);
        button.addEventListener("click", () => {
          activeLecture = index;
          showVideo();
        });
        lectureList.append(button);
      });
    }

    function open() {
      overlay.hidden = false;
      document.body.classList.add("lvp-open");
      showVideo();
    }

    function closePlayer() {
      overlay.hidden = true;
      videoBox.replaceChildren(el("div", "lvp-placeholder", "Lecture select करें"));
      document.body.classList.remove("lvp-open");
    }

    search.addEventListener("input", () => {
      searchText = search.value.trim().toLowerCase();
      renderLectures();
    });

    prev.addEventListener("click", () => {
      if (activeLecture > 0) {
        activeLecture--;
        showVideo();
      }
    });

    next.addEventListener("click", () => {
      if (activeLecture < teachers[activeTeacher].lectures.length - 1) {
        activeLecture++;
        showVideo();
      }
    });

    done.addEventListener("click", () => {
      const lecture = current();
      if (!lecture) return;
      completed[lecture.id] = !completed[lecture.id];
      save();
      showVideo();
    });

    full.addEventListener("click", () => {
      if (videoBox.requestFullscreen) {
        videoBox.requestFullscreen().catch(() => {});
      } else {
        status.textContent = "इस browser में fullscreen उपलब्ध नहीं है।";
      }
    });

    close.addEventListener("click", closePlayer);
    overlay.addEventListener("click", event => {
      if (event.target === overlay) closePlayer();
    });

    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && !overlay.hidden) closePlayer();
    });

    renderFolders();

    if (last.teacher < teachers.length &&
        last.teacher >= 0 &&
        last.lecture >= 0 &&
        last.lecture < teachers[last.teacher].lectures.length) {
      activeTeacher = last.teacher;
      activeLecture = last.lecture;
    }

    renderFolders();
    renderLectures();

    return {
      open,
      close: closePlayer,
      play: function (teacherIndex, lectureIndex) {
        if (teacherIndex >= 0 && teacherIndex < teachers.length) {
          activeTeacher = teacherIndex;
        }
        if (lectureIndex >= 0 &&
            lectureIndex < teachers[activeTeacher].lectures.length) {
          activeLecture = lectureIndex;
        }
        open();
      }
    };
  }

  window.LoyalVideoPlayer = { mount };
})();
