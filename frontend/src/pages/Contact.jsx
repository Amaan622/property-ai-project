import { FaPhone, FaEnvelope, FaGithub, FaLinkedin } from "react-icons/fa";

function Contact() {
  return (
    <div className="page contact-page">

      <h2>📞 Contact Us</h2>

      <div className="contact-card">

        <p>
          <FaPhone className="icon" />
          <b> Phone:</b> +91 70704 43800
        </p>

        <p>
          <FaEnvelope className="icon" />
          <b> Email:</b> amaanmd622@gmail.com
        </p>

        <p>
          <FaGithub className="icon" />
          <b> GitHub:</b>{" "}
          <a
            href="https://github.com/Amaan622"
            target="_blank"
            rel="noreferrer"
          >
            github.com/Amaan622
          </a>
        </p>

        <p>
          <FaLinkedin className="icon" />
          <b> LinkedIn:</b>{" "}
          <a
            href="https://www.linkedin.com/in/mdamaanrahman/"
            target="_blank"
            rel="noreferrer"
          >
            linkedin.com/in/mdamaanrahman
          </a>
        </p>

      </div>

    </div>
  );
}

export default Contact;