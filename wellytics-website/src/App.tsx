import React from "react";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Index } from "./pages/index";
import { Form } from "./pages/Form";
import { Panel } from "./pages/Panel";
import { NotFound } from "./pages/NotFound";
import { Login } from "./pages/Login";

const router = createBrowserRouter([
  {
    path: "/",
    element: <Index />,
  },
  {
    path: "/form",
    element: <Form />,
  },
  {
    path: "/login",
    element: <Login />,
  },
  {
    path: "panel",
    element: <Panel />,
  },
  {
    path: "*",
    element: <NotFound />,
  },
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
