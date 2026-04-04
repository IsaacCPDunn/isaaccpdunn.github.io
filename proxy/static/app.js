const form = document.getElementById("proxy-form");
const urlInput = document.getElementById("url");
const meta = document.getElementById("meta");
const content = document.getElementById("content");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const url = urlInput.value.trim();
  if (!url) return;

  meta.textContent = "Loading...";
  content.textContent = "";

  try {
    const response = await fetch(`/api/fetch?url=${encodeURIComponent(url)}`);
    const payload = await response.json();

    if (!response.ok || !payload.ok) {
      meta.textContent = `Error: ${payload.error ?? "Unknown error"}`;
      content.textContent = "";
      return;
    }

    meta.textContent = `Fetched ${payload.final_url} (status ${payload.status_code}, ${payload.content_type})`;
    content.textContent = payload.body;
  } catch (error) {
    meta.textContent = `Error: ${error}`;
    content.textContent = "";
  }
});
