import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Journals() {

	const [error, setError] = useState('');
	const [journals, setJournals] = useState([]);

	useEffect(
		() => {
			axios.get('http://localhost:8000/journals')
				.then((response) => {
					const journalsObject = response.data.Data;
					const keys = Object.keys(journalsObject);
					const journalsArray = keys.map((key) => journalsObject[key]);
					setJournals(journalsArray);
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
				Journals
			</h1>
			
			{error && (
				<div className="error-message">
					{error}
				</div>
			)}

			{journals.map((journal) => (
				<div className="category-container">
					 <h2>{journal.title}</h2>
					 <p>Timestamp: {journal.timestamp}</p>
				</div>
			))}
		</div>
	);
}

export default Journals;
