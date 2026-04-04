(() => {
  "use strict";

  // Compatibility stub for legacy campaign pages.
  // Keeps script loading clean while sponsor lead capture is wired later.
  window.FFSponsorLeads = window.FFSponsorLeads || {
    version: "stub-v1",
    track() { return false; },
    init() { return true; },
  };
})();
