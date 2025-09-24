module.exports = {
  testEnvironment: "jsdom",
  transform: { "^.+\\.(t|j)sx?$": ["ts-jest", { tsconfig: "tsconfig.json" }] },
  setupFilesAfterEnv: ["@testing-library/jest-dom"],
  moduleNameMapper: {},
};
