// Firebase configuration setup
// Get environment variables from Replit's environment
const getEnvVar = (name) => {
    // Try multiple ways to access environment variables in Replit
    if (typeof window !== 'undefined' && window.process && window.process.env) {
        return window.process.env[name];
    }
    if (typeof process !== 'undefined' && process.env) {
        return process.env[name];
    }
    // For Replit, environment variables are often available on window
    if (typeof window !== 'undefined' && window[name]) {
        return window[name];
    }
    return null;
};

const apiKey = getEnvVar('VITE_FIREBASE_API_KEY');
const projectId = getEnvVar('VITE_FIREBASE_PROJECT_ID');
const appId = getEnvVar('VITE_FIREBASE_APP_ID');

window.FIREBASE_CONFIG = {
    apiKey: apiKey,
    authDomain: `${projectId}.firebaseapp.com`,
    databaseURL: `https://${projectId}-default-rtdb.firebaseio.com/`,
    projectId: projectId,
    storageBucket: `${projectId}.firebasestorage.app`,
    messagingSenderId: "123456789012",
    appId: appId
};

console.log('Firebase Config Loaded:', {
    projectId: window.FIREBASE_CONFIG.projectId,
    hasApiKey: !!window.FIREBASE_CONFIG.apiKey,
    hasAppId: !!window.FIREBASE_CONFIG.appId
});
