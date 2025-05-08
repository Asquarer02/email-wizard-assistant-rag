document.getElementById("chat-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const input = document.getElementById("query-input");
  const chat = document.getElementById("chat");
  const userQuery = input.value.trim();

  if (!userQuery) return;

  
  chat.innerHTML += `<div class='text-right'><span class='bg-blue-600 inline-block px-4 py-2 rounded-xl mb-2'>${userQuery}</span></div>`;
  chat.scrollTop = chat.scrollHeight;

  
  input.value = "";

  
  try {
    const res = await fetch("/query_email", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query: userQuery }),
    });

    const data = await res.json();

    if (res.ok) {
      chat.innerHTML += `<div class='text-left'><span class='bg-gray-700 inline-block px-4 py-2 rounded-xl mb-2'>${data.response}</span></div>`;
    } else {
      chat.innerHTML += `<div class='text-left text-red-400'><span>Error: ${data.error}</span></div>`;
    }
  } catch (err) {
    chat.innerHTML += `<div class='text-left text-red-400'><span>Network error. Try again later.</span></div>`;
  }

  chat.scrollTop = chat.scrollHeight;
});
