import React, { useState, useEffect } from "react";
import { Navigate } from "react-router-dom";

export const ProtectedRoute = ({ children, isAuthenticated }) => {
	const [authenticated, setAuthenticated] = useState(false);
	const [loading, setLoading] = useState(true);

	useEffect(() => {
		const checkAuthentication = async () => {
			try {
				setLoading(true);
				const authenticated = await isAuthenticated();
				setAuthenticated(authenticated);
			} catch (error) {
				console.error("Error al verificar la autenticación:", error);
				setAuthenticated(false);
			} finally {
				setLoading(false);
			}
		};

		checkAuthentication();
	}, [isAuthenticated]);

	if (loading) {
		return (
			<div className="flex justify-center items-center h-screen">
				<div className="loader ease-linear rounded-full border-8 border-t-8 border-gray-200 h-24 w-24"></div>
			</div>
		);
	}

	if (!authenticated) {
		return <Navigate to="/SignIn" replace />;
	} else {
		return children;
	}
};
