"use strict";
(() => {
  const scenario = window.CIVICSHIELD_SCENARIO;
  if (!scenario || scenario.is_synthetic !== true || scenario.is_official_warning !== false ||
      scenario.external_services_called !== false || scenario.database_reports_created !== 0 ||
      scenario.samples.length !== 24 || scenario.chapters.length !== 4) {
    document.querySelector("#stage-explanation").textContent =
      "Offline data integrity check failed. No exercise can be displayed.";
    return;
  }

  const $ = (selector) => document.querySelector(selector);
  const ns = "http://www.w3.org/2000/svg";
  const samples = scenario.samples;
  const svg = $("#chart");
  const w = 810, x0 = 52, x1 = 772, baseline = 242, top = 35;
  const xp = (i) => x0 + (i * (x1-x0)/23);
  const ypRain = (v) => baseline - (v / 16) * (baseline-top);
  const ypReports = (v) => baseline - (v / 5) * (baseline-top);
  const el = (tag, attrs = {}, text = "") => {
    const elem = document.createElementNS(ns, tag);
    Object.entries(attrs).forEach(([key,val]) => elem.setAttribute(key, String(val)));
    if (text) elem.textContent = text;
    return elem;
  };
  $("#metric-hours").textContent = scenario.summary.hours + " h";
  $("#metric-rain").textContent = scenario.summary.invented_precipitation_total_mm + " mm";
  $("#metric-reports").textContent = String(scenario.summary.invented_report_total);

  const rows = $("#data-rows");
  for (const point of samples) {
    const tr = document.createElement("tr");
    [String(point.hour).padStart(2,"0") + ":00",point.invented_hourly_precipitation_mm,point.invented_report_count]
      .forEach(value => {
        const td = document.createElement("td");
        td.textContent = String(value);
        tr.appendChild(td);
      });
    rows.appendChild(tr);
  }

  function draw(selectedHour) {
    svg.replaceChildren();
    for (let n=0; n<=4; n++) {
      const y = baseline - n * (baseline-top)/4;
      svg.appendChild(el("line",{x1:x0-12,y1:y,x2:x1+10,y2:y,stroke:"#294663","stroke-width":1}));
      svg.appendChild(el("text",{x:8,y:y+4,"font-size":12,fill:"#b2cbdf"},String(n*4)));
    }
    samples.forEach((item,i) => {
      const x = xp(i), y = ypReports(item.invented_report_count);
      svg.appendChild(el("rect",{x:x-6,y:y,width:12,height:baseline-y,rx:3,fill:"#efb16c",opacity:.65}));
      if (i % 4 === 0 || i === 23) {
        svg.appendChild(el("text",{x,y:270,fill:"#9fbed9","font-size":12,"text-anchor":"middle"},String(i).padStart(2,"0")));
      }
    });
    const points = samples.map((item,i)=>xp(i)+","+ypRain(item.invented_hourly_precipitation_mm)).join(" ");
    svg.appendChild(el("polyline",{points,fill:"none",stroke:"#68c5ff","stroke-width":3,"stroke-linejoin":"round"}));
    const s = samples[selectedHour];
    svg.appendChild(el("line",{x1:xp(selectedHour),y1:top-10,x2:xp(selectedHour),y2:baseline,stroke:"#a7d7ff","stroke-dasharray":"5 5",opacity:.9}));
    svg.appendChild(el("circle",{cx:xp(selectedHour),cy:ypRain(s.invented_hourly_precipitation_mm),r:7,fill:"#68c5ff",stroke:"#10213b","stroke-width":3}));
    $("#hour-label").textContent = String(selectedHour).padStart(2,"0") + ":00 UTC";
    $("#selected-hour").textContent = String(selectedHour).padStart(2,"0") + ":00";
    $("#selected-rain").textContent = s.invented_hourly_precipitation_mm + " mm/h";
    $("#selected-reports").textContent = String(s.invented_report_count);
  }

  const stages = $("#stages");
  function selectStage(index) {
    scenario.chapters.forEach((chapter, i) => {
      stages.children[i].setAttribute("aria-pressed", String(i===index));
    });
    const selected = scenario.chapters[index];
    $("#stage-time").textContent = "Fictional hour " + selected.hour;
    $("#stage-title").textContent = selected.title;
    $("#stage-explanation").textContent = selected.explanation;
    $("#takeaway").textContent = "Engineering takeaway: " + selected.operator_takeaway;
    $("#hour-slider").value = String(selected.hour);
    draw(selected.hour);
  }
  scenario.chapters.forEach((chapter,i) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "stage";
    button.textContent = chapter.title;
    button.setAttribute("aria-pressed", "false");
    button.addEventListener("click", () => selectStage(i));
    stages.appendChild(button);
  });
  $("#hour-slider").addEventListener("input", (event) => draw(Number(event.target.value)));
  selectStage(2);
})();
