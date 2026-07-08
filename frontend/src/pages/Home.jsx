import BugForm from "../components/BugForm";

function Home() {
  return (
    <div className="container">
      <h1>AI Smart Bug Analyzer & Fix Advisor</h1>
      <p>AI-Powered Bug Analysis, File Parsing & Intelligent Fix Recommendations</p>

      <BugForm />
    </div>
  );
}

export default Home;