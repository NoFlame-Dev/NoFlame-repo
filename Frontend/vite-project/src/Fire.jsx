import React from "react";
import "./Fire.css";
import firePng from "./assets/fire.png"

const Fire = () => {
    return (
        <div className="fire">
            <img src={firePng} alt="Fire" className="flame flame1" />
            <img src={firePng} alt="Fire" className="flame flame2" />
            <img src={firePng} alt="Fire" className="flame flame3" />
        </div>
    );
};

export default Fire;