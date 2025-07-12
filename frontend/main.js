const BASE_URL = "http://localhost:5000";

document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const email = document.getElementById("email").value;
      const password = document.getElementById("password").value;

      const res = await fetch(`${BASE_URL}/api/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();
      if (data.success) {
        localStorage.setItem("user", JSON.stringify(data));
        alert("Login successful!");
        if (data.is_admin) {
          window.location.href = "admin.html";
        } else {
          window.location.href = "profile.html";
        }
      } else {
        alert("Login failed: " + data.message);
      }
    });
  }
});


  const registerForm = document.getElementById("registerForm");
  if (registerForm) {
    registerForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const name = document.getElementById("name").value;
      const email = document.getElementById("regEmail").value;
      const password = document.getElementById("regPassword").value;

      const res = await fetch(`${BASE_URL}/api/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await res.json();
      if (data.success) {
        alert("Registration successful! Please log in.");
        window.location.href = "login.html";
      } else {
        alert("Registration failed: " + data.message);
      }
    });
  }


  const profileForm = document.getElementById("profileForm");
  if (profileForm) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
      alert("Please login first");
      window.location.href = "login.html";
    }

    profileForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const payload = {
        user_id: user.user_id,
        name: document.getElementById("name").value,
        location: document.getElementById("location").value,
        skills_offered: document.getElementById("skills_offered").value,
        skills_wanted: document.getElementById("skills_wanted").value,
        availability: document.getElementById("availability").value,
        is_public: document.getElementById("is_public").checked,
      };

      const res = await fetch(`${BASE_URL}/api/profile/update`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const data = await res.json();
      if (data.success) {
        alert("Profile updated successfully!");
      } else {
        alert("Error: " + data.message);
      }
    });
  }


  const sentList = document.getElementById("sentRequests");
  const receivedList = document.getElementById("receivedRequests");

  if (sentList && receivedList) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
      alert("Login required");
      window.location.href = "login.html";
    }

    // Fetch swaps
    fetch(`${BASE_URL}/api/swap-requests/${user.user_id}`)
      .then(res => res.json())
      .then(data => {
        renderSwaps(data.sent_requests, sentList, false);
        renderSwaps(data.received_requests, receivedList, true);
      });

    function renderSwaps(list, container, isReceived) {
      container.innerHTML = "";
      if (list.length === 0) {
        container.innerHTML = "<p class='text-gray-500'>No requests yet.</p>";
        return;
      }

      list.forEach(item => {
        const li = document.createElement("li");
        li.className = "p-4 border rounded bg-gray-50";
        li.innerHTML = `
          <p><strong>Offered:</strong> ${item.offered_skill}</p>
          <p><strong>Wanted:</strong> ${item.wanted_skill}</p>
          <p><strong>Status:</strong> <span class="font-semibold">${item.status}</span></p>
        `;

        if (item.status === "pending") {
          const btnGroup = document.createElement("div");
          btnGroup.className = "mt-2 space-x-2";

          if (isReceived) {
            ["accepted", "rejected"].forEach(status => {
              const btn = document.createElement("button");
              btn.textContent = status.charAt(0).toUpperCase() + status.slice(1);
              btn.className = `px-3 py-1 rounded text-white ${
                status === "accepted" ? "bg-green-600" : "bg-red-600"
              }`;
              btn.onclick = () => updateStatus(item.id, status);
              btnGroup.appendChild(btn);
            });
          } else {
            const delBtn = document.createElement("button");
            delBtn.textContent = "Delete";
            delBtn.className = "px-3 py-1 rounded bg-gray-600 text-white";
            delBtn.onclick = () => updateStatus(item.id, "deleted");
            btnGroup.appendChild(delBtn);
          }

          li.appendChild(btnGroup);
        }

        container.appendChild(li);
      });
    }

    function updateStatus(id, status) {
      fetch(`${BASE_URL}/api/swap-request/${id}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ status }),
      })
        .then(res => res.json())
        .then(data => {
          alert(data.message);
          location.reload();
        });
    }
  }


  const searchForm = document.getElementById("searchForm");
  const searchResults = document.getElementById("searchResults");

  if (searchForm && searchResults) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user) {
      alert("Please log in first");
      window.location.href = "login.html";
    }

    searchForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const skill = document.getElementById("skillSearch").value;

      const res = await fetch(`${BASE_URL}/api/public-profiles?skill=${skill}`);
      const data = await res.json();

      searchResults.innerHTML = "";

      if (data.users.length === 0) {
        searchResults.innerHTML = "<p class='text-gray-500'>No matches found.</p>";
        return;
      }

      data.users.forEach(u => {
        if (u.id === user.user_id) return; // Skip own profile

        const li = document.createElement("li");
        li.className = "p-4 border rounded bg-gray-50";

        li.innerHTML = `
          <p><strong>${u.name}</strong> (${u.location || "Unknown"})</p>
          <p><strong>Offers:</strong> ${u.skills_offered}</p>
          <p><strong>Wants:</strong> ${u.skills_wanted}</p>
          <p><strong>Available:</strong> ${u.availability}</p>
        `;

        const btn = document.createElement("button");
        btn.textContent = "Request Swap";
        btn.className = "mt-2 px-3 py-1 rounded bg-green-600 text-white";
        btn.onclick = () => {
          const offered = prompt("Which skill do YOU offer?");
          const wanted = prompt("Which skill do you WANT from them?");
          if (offered && wanted) {
            requestSwap(user.user_id, u.id, offered, wanted);
          }
        };

        li.appendChild(btn);
        searchResults.appendChild(li);
      });
    });

    async function requestSwap(fromId, toId, offered, wanted) {
      const res = await fetch(`${BASE_URL}/api/request-swap`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          from_user_id: fromId,
          to_user_id: toId,
          offered_skill: offered,
          wanted_skill: wanted,
        }),
      });

      const data = await res.json();
      alert(data.message);
    }
  }


  const stats = document.getElementById("stats");
  const banForm = document.getElementById("banForm");

  if (stats && banForm) {
    const user = JSON.parse(localStorage.getItem("user"));
    if (!user || !user.is_admin) {
      alert("Admin access required");
      window.location.href = "login.html";
    }

    // Load platform stats
    fetch(`${BASE_URL}/api/admin/stats`)
      .then(res => res.json())
      .then(data => {
        document.getElementById("statUsers").textContent = data.total_users;
        document.getElementById("statSwaps").textContent = data.total_swaps;
        document.getElementById("statFeedback").textContent = data.total_feedback;
      });

    // Ban user
    banForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const id = document.getElementById("banUserId").value;

      const res = await fetch(`${BASE_URL}/api/admin/ban-user/${id}`, {
        method: "POST",
      });

      const data = await res.json();
      alert(data.message);
    });
  }

  // Download CSV logs
  function downloadCSV() {
    window.open(`${BASE_URL}/api/admin/export-feedback`, "_blank");
  }


function toggleTheme() {
  const htmlEl = document.documentElement;
  const isDark = htmlEl.classList.toggle("dark");
  localStorage.theme = isDark ? "dark" : "light";
}
