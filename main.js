const { app, BrowserWindow } = require("electron");

function createWindow() {
  const win = new BrowserWindow({
    width: 320,
    height: 480,
    resizable: false,
    maximizable: false,
    fullscreenable: false,
    frame: false,
    webPreferences: {
      contextIsolation: true,
    },
  });

  win.loadFile("index.html");
//   win.webContents.openDevTools();
}

app.whenReady().then(createWindow);

app.on("window-all-closed", () => {
  if (process.platform !== "darwin") app.quit();
});

