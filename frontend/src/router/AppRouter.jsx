import React from "react";
import { Routes, Route } from "react-router-dom";

import { Home } from "../home/pages/Home";

import { SignIn } from "../auth/pages/SignIn";
import { SignUp } from "../auth/pages/SignUp";

import { NotFound } from "../404";

import { ProtectedRoute } from "./ProtectedRoute";

import axios from "axios";

function getCookie(name) {
	const value = `; ${document.cookie}`;
	const parts = value.split(`; ${name}=`);
	if (parts.length === 2) return parts.pop().split(";").shift();
}

const isAuthenticated = async () => {
	try {
		const token = getCookie("token");
		const response = await axios.post(
				`${import.meta.env.VITE_BACKEND_URL}/api/auth/`,
			{
				token,
			},
			{
				headers: {
					accept: "application/json",
					"Content-Type": "application/json",
				},
			}
		);
		return response.status === 200;
	} catch (error) {
		console.error("Error al verificar la autenticación:", error);
		return false;
	}
};

const AppRouter = () => {
	return (
		<Routes>
			<Route path="/" element={<Home />} />

			<Route path="/SignIn" element={<SignIn />} />
			<Route path="/signup" element={<SignUp />} />

			<Route
				path="/home"
				element={
					<ProtectedRoute isAuthenticated={isAuthenticated}>
						<Home />
					</ProtectedRoute>
				}
			/>

			<Route path="/*" element={<NotFound />} />
		</Routes>
	);
};

export default AppRouter;
