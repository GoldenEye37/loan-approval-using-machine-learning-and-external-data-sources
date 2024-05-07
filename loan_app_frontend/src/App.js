import './App.css';
import {Component} from "react";
import Home from "./pages/Home";
import {Navigate, Outlet, Route, Routes} from "react-router-dom";

function App() {
  return (
      <main className="flex items-center justify-center h-screen m-6">
        <Routes>
          <Route path="/" element={<Navigate to="/home"/>}/>
        </Routes>
        <Outlet/>
      </main>);
}

export default App;
