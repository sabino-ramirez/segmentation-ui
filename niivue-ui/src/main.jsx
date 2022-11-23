import React from "react";
import ReactDOM from "react-dom";
// import { Container } from "@mui/material";
import { CssBaseline } from "@mui/material";
import "./index.css";
import NiiVue from "./Niivue";
import MyNiiVue from "./myNiivue";
import Doc3d from "./doc3d";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";

const volumes = [
  // { url: "./mni152reallyreallyreallyreallyreallyLongName.nii" },
  // { url: "./hippo.nii" },
  // { url: "/pt19.nii.gz" },
  // { url: "/pt19_label.nii.gz", colorMap: "green" },
];
ReactDOM.render(
  <React.StrictMode>
    <MyNiiVue />
  </React.StrictMode>,
  document.getElementById("root")
);
