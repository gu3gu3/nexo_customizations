frappe.ready(() => {
	const targets = new Set(["#forgot", "#login", "#login-with-email-link"]);
	const links = Array.from(document.querySelectorAll("a")).filter((link) => targets.has(link.getAttribute("href")));
	const target = document.querySelector(".nexo-login-card");
	if (!links.length || !target) return;

	links.forEach((link) => {
		link.addEventListener("click", () => {
			target.scrollIntoView({ behavior: "smooth", block: "center" });
		});
	});
});
