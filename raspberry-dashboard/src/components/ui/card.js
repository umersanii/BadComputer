import React from "react";

const Card = ({ children }) => (
  <div className="bg-gray-800 p-4 rounded-xl shadow-md">{children}</div>
);

const CardContent = ({ children }) => <div className="p-2">{children}</div>;

export { Card, CardContent };
