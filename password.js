window.onload = function() {
    document.getElementById("generate").onclick = function() {
        const chars = document.getElementById("chars").value;
        const min = document.getElementById("min").value;
        const max = document.getElementById("max").value;
        const length = Math.floor(Math.random() * (max - min + 1) + min);
        let password = "";
        while (password.length < length) {
            password += chars.charAt(Math.floor(Math.random() * chars.length));
        }
        document.getElementById("password").value = password;
    }
    document.getElementById("copy").onclick = function() {
        document.getElementById("password").select();
        document.execCommand("copy");
    }
}