import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const Private = () => {
    const navigate = useNavigate();
    const [message, setMessage] = useState("");

    useEffect(() => {
        const token = sessionStorage.getItem("token");
        console.log("TOKEN ENVIADO:", token);

        if (!token) {
            alert("Debes iniciar sesión para acceder.");
            return navigate("/login");
        }

        fetch("https://super-potato-5gxr57xj6wpj3vq9p-3001.app.github.dev/api/private", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token,
                "Content-Type": "application/json"
            }
        })
            .then(async (res) => {
                if (!res.ok) {
                    const errorData = await res.json();
                    throw new Error(errorData.msg || "Error al acceder al recurso");
                }
                return res.json();
            })
            .then((data) => setMessage(data.msg))
            .catch((err) => {
                alert(err.message);
                navigate("/login");
            });
    }, []);

    return (
        <div className="container mt-5">
            <h2>Zona Privada</h2>
            <p>{message || "Cargando..."}</p>
            <button className="btn btn-danger mt-3" onClick={() => {
                sessionStorage.removeItem("token");
                alert("Sesión cerrada");
                navigate("/login");
            }}>
                Cerrar Sesión
            </button>
        </div>
    );

};



export default Private;
