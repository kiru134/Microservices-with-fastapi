import { BrowserRouter, Routes, Route } from "react-router-dom";
import "./App.css";
import Products from "./routes/products";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Products />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
