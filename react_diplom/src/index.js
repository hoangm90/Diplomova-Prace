import ReactDOM from "react-dom";
import React from "react";
import { BrowserRouter } from "react-router-dom";

import App from "./App";

const Home = () => {
 
  return (
    <BrowserRouter>
      <App />
    </BrowserRouter>
  );
};

ReactDOM.render(<Home />, document.getElementById("root"));