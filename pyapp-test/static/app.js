const clockEl = document.getElementById("clock");
const tzEl = document.getElementById("tz");

async function refreshTime() {
  try {
    const response = await fetch("/api/time", { cache: "no-store" });
    const data = await response.json();

    clockEl.textContent = data.time;
    tzEl.textContent = `Timezone: ${data.timezone} (UTC${formatOffset(data.utc_offset)})`;
  } catch (error) {
    clockEl.textContent = "Unable to load server time";
    console.error(error);
  }
}

function formatOffset(rawOffset) {
  if (!rawOffset || rawOffset.length !== 5) {
    return "";
  }

  return `${rawOffset.slice(0, 3)}:${rawOffset.slice(3)}`;
}

refreshTime();
setInterval(refreshTime, 1000);
