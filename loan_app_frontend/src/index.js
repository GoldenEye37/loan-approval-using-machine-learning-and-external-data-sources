import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';
import {createBrowserRouter, RouterProvider} from "react-router-dom";
import ErrorPage from "./pages/ErrorPage";
import App from "./App";
import LoanPage from "./pages/LoanPage";


// first thing is to create a BrowserRouter instance using the createBrowserRouter function
// from react-router-dom. This function takes an array of route objects as an argument.

const router = createBrowserRouter([
    {
        path: '/',
        element: <App />,
        errorElement: <ErrorPage />,
        children: [
        { path: 'loan-approval', element: <LoanPage /> },
        ],
    },
    ]);

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    {/*<RouterProvider router={router} />*/}
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
