import {
  BrowserRouter,
  Routes,
  Route,
} from 'react-router-dom';

import './App.css';

import Navbar from './Components/Navbar';
import Categories from './Components/Categories';
import Users from './Components/Users';
import Journals from './Components/Journals';

function App() {
  return (
    <BrowserRouter>
      <Navbar/>
      <Routes>
        <Route path="" element={<h1>Home</h1>} />
        <Route path="categories" element={ <Categories/> } />
        <Route path="users" element={ <Users/> } />
        <Route path="journals" element={ <Journals/> } />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
