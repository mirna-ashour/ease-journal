import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Users() {

	const [error, setError] = useState('');
	const [users, setUsers] = useState([]);

	useEffect(
		() => {
			axios.get('http://localhost:8000/users')
				.then((response) => {
					const usersObject = response.data.Data;
					const keys = Object.keys(usersObject);
					const usersArray = keys.map((key) => usersObject[key]);
					setUsers(usersArray);
				}) // something good
				.catch(() => {
					setError('Something went wrong'); 
				}); // something bad
		},
		[],
	);

	return (
		<div className="wrapper">
			<h1>
				Users
			</h1>
			
			{error && (
				<div className="error-message">
					{error}
				</div>
			)}

			{users.map((user) => (
				<div className="user-container">
					 <h2>{user.first_name}</h2>
					 <p>Date of Birth: {user.dob}</p>
				</div>
			))}
		</div>
	);
}

export default Users;
