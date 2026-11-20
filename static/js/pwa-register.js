if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js", { scope: "/" })
      .catch((error) => {
        console.warn("LOYAL PWA registration failed:", error);
      });
  });
}
