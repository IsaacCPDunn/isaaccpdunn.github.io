function randomIntInclusive(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

function setStatus(message, type = "") {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = type;
}

function generatePassword(chars, min, max) {
    const length = randomIntInclusive(min, max);
    let password = "";

    for (let i = 0; i < length; i += 1) {
        const index = Math.floor(Math.random() * chars.length);
        password += chars.charAt(index);
    }

    return password;
}

window.addEventListener("DOMContentLoaded", () => {
    const charsInput = document.getElementById("chars");
    const minInput = document.getElementById("min");
    const maxInput = document.getElementById("max");
    const passwordOutput = document.getElementById("password");
    const generateBtn = document.getElementById("generate");
    const copyBtn = document.getElementById("copy");

    generateBtn.addEventListener("click", () => {
        const chars = charsInput.value;
        const min = Number.parseInt(minInput.value, 10);
        const max = Number.parseInt(maxInput.value, 10);

        if (!chars) {
            setStatus("Please enter at least one allowed character.", "error");
            passwordOutput.value = "";
            return;
        }

        if (!Number.isInteger(min) || !Number.isInteger(max)) {
            setStatus("Please enter valid minimum and maximum lengths.", "error");
            passwordOutput.value = "";
            return;
        }

        if (min < 1 || max < 1) {
            setStatus("Length values must be at least 1.", "error");
            passwordOutput.value = "";
            return;
        }

        if (min > max) {
            setStatus("Minimum length cannot be greater than maximum length.", "error");
            passwordOutput.value = "";
            return;
        }

        const password = generatePassword(chars, min, max);
        passwordOutput.value = password;
        setStatus(`Generated password with ${password.length} characters.`, "success");
    });

    copyBtn.addEventListener("click", async () => {
        const value = passwordOutput.value;

        if (!value) {
            setStatus("Generate a password before copying.", "error");
            return;
        }

        try {
            await navigator.clipboard.writeText(value);
            setStatus("Password copied to clipboard.", "success");
        } catch {
            passwordOutput.select();
            passwordOutput.setSelectionRange(0, value.length);
            const copied = document.execCommand("copy");
            setStatus(copied ? "Password copied to clipboard." : "Unable to copy automatically.", copied ? "success" : "error");
        }
    });
});
