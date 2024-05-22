import React from "react";
import { Routes, Route } from "react-router-dom";

import { Home } from "../home/pages/Home";
import { NotFound } from "../404";
import { Blog } from "../home/pages/Blog"; // Importa el nuevo componente

const AppRouter = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/blog/:id" element={<Blog />} /> {/* Ruta dinámica */}
      <Route path="/*" element={<NotFound />} />
    </Routes>
  );
};

export default AppRouter;
