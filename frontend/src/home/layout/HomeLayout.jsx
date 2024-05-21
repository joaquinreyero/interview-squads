import React from "react";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

export const HomeLayout = ({ children }) => {
	return (
		<>
			<Navbar />
			<div className="mx-auto max-w-screen-2xl">{children}</div>
			<Footer />
		</>
	);
};

export default HomeLayout;
