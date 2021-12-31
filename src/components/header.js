import { Link } from 'gatsby';
import PropTypes from 'prop-types';
import React from 'react';

import Nav from './nav';

const Header = ({ siteTitle }) => (
  <header>
    <div className="header__title">
      <h1>
        <Link to="/">{siteTitle}</Link>
      </h1>
    </div>
    <Nav />
  </header>
);

Header.propTypes = {
  siteTitle: PropTypes.string,
};

Header.defaultProps = {
  siteTitle: ``,
};

export default Header;