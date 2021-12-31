import React from 'react';
import { Link } from 'gatsby';

const Nav = ({ buttonText }) => {
  return (
    <nav>
      <Link to="/about">About</Link>
      <Link to="/blog">Blog</Link>
      <Link to="/projects">Projects</Link>
      <Link to="https://github.com/jflick58">Github</Link>
      <Link to="https://www.linkedin.com/in/justin-flick-88416b71">Linkedin</Link>
    </nav>
  );
};

export default Nav;