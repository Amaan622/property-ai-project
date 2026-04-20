import { Link } from "react-router-dom";

function Header() {
  return (
    <div className="header">
      
      {/* Logo -> Home */}
      <h1>
        <Link to="/" className="logo">
          🏡 Property AI
        </Link>
      </h1>

      {/* Navigation */}
      <nav>
        <Link to="/">Home</Link>
        <Link to="/help">Help</Link>
        <Link to="/contact">Contact</Link>
      </nav>

    </div>
  );
}

export default Header;