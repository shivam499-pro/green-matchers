export default {
  name: "Green Matchers",
  slug: "green-matchers-mobile",
  version: "1.0.0",
  orientation: "portrait",
  icon: "./assets/icon.png",
  userInterfaceStyle: "light",
  splash: {
    image: "./assets/splash.png",
    resizeMode: "contain",
    backgroundColor: "#4CAF50"
  },
  assetBundlePatterns: [
    "**/*"
  ],
  ios: {
    supportsTablet: true
  },
  android: {
    adaptiveIcon: {
      foregroundImage: "./assets/adaptive-icon.png",
      backgroundColor: "#4CAF50"
    },
    package: "com.anonymous.greenmatchersmobile"
  },
  web: {
    favicon: "./assets/favicon.png"
  },
  sdkVersion: "54.0.0",
  platforms: ["android", "ios"],
  runtimeVersion: {
    policy: "sdkVersion"
  }
};