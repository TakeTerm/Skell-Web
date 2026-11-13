const OBSERVER_MARGIN = "700px 0px";

export function whenNearViewport(element, callback) {
  if (!("IntersectionObserver" in window)) {
    callback();
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      observer.disconnect();
      callback();
    },
    { rootMargin: OBSERVER_MARGIN }
  );
  observer.observe(element);
}

export function whileVisible(element, onChange) {
  if (!("IntersectionObserver" in window)) {
    onChange(true);
    return;
  }
  new IntersectionObserver((entries) => onChange(entries.at(-1).isIntersecting)).observe(element);
}
