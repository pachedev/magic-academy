import React from 'react';

interface Card {
	id: number;
	name: string;
	last_name: string;
	identification: string;
	age: number;
	magic_affinity: any;
	state: any;
}

const CardComponent: React.FC<{ card: Card }> = ({ card }) => {
	return (
		<div className="bg-white shadow-lg rounded-lg p-2 mb-2 hover:bg-gray-100">
			<div className="text-sm text-gray-600">ID: {card.id}</div>
			<div className="text-lg font-semibold text-gray-800">{card.name} {card.last_name}</div>
			<div className="text-sm text-gray-700">Identificador: {card.identification}</div>
			<div className="text-md text-gray-700">Edad: {card.age}</div>
			<div className="text-md text-gray-700">Afinidad mágica: {card.magic_affinity?.value}</div>
			<div className="text-md text-gray-700">Estado: {card.state?.value}</div>
		</div>
	);
};

export default CardComponent;