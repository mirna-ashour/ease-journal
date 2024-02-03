import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Categories() {

	const [error, setError] = useState('');
	const [categories, setCategories] = useState([]);

	useEffect(
		() => {
			axios.get('http://localhost:8000/categories')
				.then((response) => {
					const categoriesObject = response.data.Data;
					const keys = Object.keys(categoriesObject);
					const categoriesArray = keys.map((key) => categoriesObject[key]);
					setCategories(categoriesArray);
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
				Categories
			</h1>
			
			{error && (
				<div className="error-message">
					{error}
				</div>
			)}

			{categories.map((category) => (
				<div className="category-container">
					 <h2>{category.title}</h2>
					 <p>Created: {category.created}</p>
				</div>
			))}
		</div>
	);
}

export default Categories;
