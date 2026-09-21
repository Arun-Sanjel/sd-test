document.addEventListener("DOMContentLoaded", () => {
  const greetingEl = document.getElementById("greeting");
  const nameInput = document.getElementById("name-input");
  const sendBtn = document.getElementById("send-btn");
  const jsonOutput = document.getElementById("json-output");
  const latencyTag = document.getElementById("latency-tag");

  // Simulated backend API endpoint handler
  async function mockApiCall(name) {
    const startTime = performance.now();

    // Simulate network latency (200ms)
    await new Promise((resolve) => setTimeout(resolve, 200));

    const endTime = performance.now();
    const duration = Math.round(endTime - startTime);

    const payload = {
      status: 200,
      endpoint: "/api/v1/hello",
      timestamp: new Date().toISOString(),
      data: {
        greeting: `Hello, ${name || "World"}!`,
        server: "Mock Static Backend",
        success: true,
      },
    };

    return { payload, duration };
  }

  async function handleSend() {
    const rawName = nameInput.value.trim();
    const targetName = rawName.length > 0 ? rawName : "World";

    sendBtn.disabled = true;
    sendBtn.textContent = "Loading...";

    try {
      const { payload, duration } = await mockApiCall(targetName);

      // Update UI
      greetingEl.textContent = payload.data.greeting;
      jsonOutput.textContent = JSON.stringify(payload, null, 2);
      latencyTag.textContent = `${duration} ms`;
    } catch (err) {
      jsonOutput.textContent = JSON.stringify({ error: err.message }, null, 2);
    } finally {
      sendBtn.disabled = false;
      sendBtn.textContent = "Send Request";
    }
  }

  sendBtn.addEventListener("click", handleSend);

  nameInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      handleSend();
    }
  });
});