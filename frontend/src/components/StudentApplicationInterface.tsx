import React, { useState, useEffect } from 'react';
import axios from 'axios';
import CardComponent from './CardComponent';

interface StudenApplication {
	id: number;
	name: string;
	last_name: string;
	identification: string;
	age: number;
	magic_affinity: any;
	state: any;
	created_at: string;
	updated_at: string;
}


interface StudentApplicationInterfaceProps {
	appName: string;
}

const StudentApplicationInterface: React.FC<StudentApplicationInterfaceProps> = ({ appName }) => {
	const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:3500';
	const [studentApplications, setStudentApplications] = useState<StudenApplication[]>([]);
	const [newStudentApplication, setNewStudentApplication] = useState({ name: '', last_name: '', identification: '', age: 0, magic_affinity: ''});
	const [updateStudentApplication, setUpdateStudentApplication] = useState({ id:'', name: '', last_name: '', identification: '', age: 0, magic_affinity: '' });
	const [changeStatusStudentApplication, setChangeStatusStudentApplication] = useState({ status:'rejected' });

	const bgColor = 'bg-yellow-500';
	const btnColor = 'bg-red-700 hover:bg-red-600';

	// Fetch student applications
	useEffect(() => {
		const fetchData = async () => {
			try {
				const response = await axios.get(`${apiUrl}/solicitudes`);
				setStudentApplications(response.data.applications.reverse());
			} catch (error) {
				console.error('Error fetching data:', error);
			}
		};

		fetchData();
	}, [appName, apiUrl]);

	// Create a student aplication
	const createStudentApplications = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		try {
			const response = await axios.post(`${apiUrl}/solicitud`, newStudentApplication);
			setStudentApplications([response.data.application, ...studentApplications]);
			setNewStudentApplication({ name: '', last_name: '', identification: '', age: 0, magic_affinity: '' });
		} catch (error) {
			console.error('Error creating user:', error);
		}
	};

	// Update a student aplication
	const handleUpdateUser = async (e: React.FormEvent<HTMLFormElement>) => {
		e.preventDefault();
		try {
			await axios.put(`${apiUrl}/solicitud/${updateStudentApplication.id}`, { name: updateStudentApplication.name, last_name: updateStudentApplication.last_name, identification: updateStudentApplication.identification, age: updateStudentApplication.age, magic_affinity: updateStudentApplication.magic_affinity });
			setUpdateStudentApplication({ id:'', name: '', last_name: '', identification: '', age: 0, magic_affinity: '' });
			setStudentApplications(
				studentApplications.map((user) => {
					if (user.id === parseInt(updateStudentApplication.id)) {
						return { ...user, name: updateStudentApplication.name, last_name: updateStudentApplication.last_name, identification: updateStudentApplication.identification, age: updateStudentApplication.age, magic_affinity: updateStudentApplication.magic_affinity };
					}
					return user;
				})
			);
		} catch (error) {
			console.error('Error updating user:', error);
		}
	};

	// Delete a student application
	const deleteStudentApplication = async (applicationId: number) => {
		try {
			await axios.delete(`${apiUrl}/solicitud/${applicationId}`);
			setStudentApplications(studentApplications.filter((application) => application.id !== applicationId));
		} catch (error) {
			console.error('Error deleting student application:', error);
		}
	};

	// Reject a student application
	const rejectStudentApplication = async (applicationId: number) => {
		try {
			await axios.patch(`${apiUrl}/solicitud/${applicationId}/status`, changeStatusStudentApplication);
		} catch (error) {
			console.error('Error reject student application:', error);
		}
	};


	return (
		<div className={`user-interface ${bgColor} w-full max-w-md p-4 my-4 rounded shadow`}>
			<img src={`/magic_academy.png`} alt={`${appName} Logo`} className="w-20 h-20 mb-6 mx-auto" />
			<h2 className="text-xl font-bold text-center text-white mb-6">{`${appName.charAt(0).toUpperCase() + appName.slice(1)} Frontend`}</h2>

			{/* Form to add new user */}
			<form onSubmit={createStudentApplications} className="mb-6 p-4 bg-blue-100 rounded shadow">
				<input
					placeholder="Nombre"
					value={newStudentApplication.name}
					onChange={(e) => setNewStudentApplication({ ...newStudentApplication, name: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Apellido"
					value={newStudentApplication.last_name}
					onChange={(e) => setNewStudentApplication({ ...newStudentApplication, last_name: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Indentificador"
					value={newStudentApplication.identification}
					onChange={(e) => setNewStudentApplication({ ...newStudentApplication, identification: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Edad"
					value={newStudentApplication.age}
					onChange={(e) => setNewStudentApplication({ ...newStudentApplication, age: parseInt(e.target.value) })}
					type='number'
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Afinidad mágica darkness,light,fire,water,wind o earth"
					value={newStudentApplication.magic_affinity}
					onChange={(e) => setNewStudentApplication({ ...newStudentApplication, magic_affinity: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<button type="submit" className="w-full p-2 text-white bg-blue-500 rounded hover:bg-blue-600">
					Envíar solicitud
				</button>
			</form>

			{/* Form to update user */}
			<form onSubmit={handleUpdateUser} className="mb-6 p-4 bg-blue-100 rounded shadow">
				<input
					placeholder="ID"
					value={updateStudentApplication.id}
					onChange={(e) => setUpdateStudentApplication({ ...updateStudentApplication, id: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Nombre"
					value={updateStudentApplication.name}
					onChange={(e) => setUpdateStudentApplication({ ...updateStudentApplication, name: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Apellido"
					value={updateStudentApplication.last_name}
					onChange={(e) => setUpdateStudentApplication({ ...updateStudentApplication, last_name: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Indentificador"
					value={updateStudentApplication.identification}
					onChange={(e) => setUpdateStudentApplication({ ...updateStudentApplication, identification: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<input
					placeholder="Edad"
					value={updateStudentApplication.age}
					onChange={(e) => setUpdateStudentApplication({ ...updateStudentApplication, age: parseInt(e.target.value) })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
					type='number'
				/>
				<input
					placeholder="Afinidad mágica darkness,light,fire,water,wind o earth"
					value={updateStudentApplication.magic_affinity}
					onChange={(e) => setUpdateStudentApplication({ ...updateStudentApplication, magic_affinity: e.target.value })}
					className="mb-2 w-full p-2 border border-gray-300 rounded text-black"
				/>
				<button type="submit" className="w-full p-2 text-white bg-green-500 rounded hover:bg-green-600">
					Actualizar solicitud
				</button>
			</form>

			{/* Display studentApplications */}
			<div className="space-y-4">
				{studentApplications.map((studentApplication) => (
					<div key={studentApplication.identification + studentApplication.id} className="flex items-center justify-between bg-white p-4 rounded-lg shadow">
						<CardComponent card={studentApplication} />
						<button onClick={() => deleteStudentApplication(studentApplication.id)} className={`${btnColor} text-white py-2 px-4 rounded`}>
							Eliminar
						</button>
					</div>
				))}
			</div>
		</div>
	);
};

export default StudentApplicationInterface;