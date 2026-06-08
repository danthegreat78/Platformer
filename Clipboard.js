async function readClipboard() {
    try{
        const text = await navigator.clipboard.readText()
        return text;
    } catch (err){
        console.error("Clipboard read failed", err);
    }
}

window.readClipboard = readClipboard;
window.writeClipboard = writeClipboard