import { app, BrowserWindow } from 'electron'
import { electronApp, optimizer } from '@electron-toolkit/utils'
import { createWindow } from './window'
import { createTray } from './tray'
import { registerIpcHandlers } from './ipc-handlers'
import { registerShortcuts, unregisterShortcuts } from './shortcuts'

// Prevent multiple instances
const gotTheLock = app.requestSingleInstanceLock()

if (!gotTheLock) {
    app.quit()
} else {
    let mainWindow: BrowserWindow | null = null

    app.whenReady().then(() => {
        // Set app user model id for windows
        electronApp.setAppUserModelId('com.eonix.jarvis')

        // Default open or close DevTools by F12 in development
        // and ignore CommandOrControl + R in production.
        app.on('browser-window-created', (_, window) => {
            optimizer.watchWindowShortcuts(window)
        })

        mainWindow = createWindow()

        // Initialize modules
        createTray(mainWindow)
        registerIpcHandlers(mainWindow)
        registerShortcuts(mainWindow)

        app.on('activate', function () {
            if (BrowserWindow.getAllWindows().length === 0) createWindow()
        })
    })

    app.on('window-all-closed', () => {
        if (process.platform !== 'darwin') {
            app.quit()
        }
    })

    app.on('will-quit', () => {
        unregisterShortcuts()
    })
}
