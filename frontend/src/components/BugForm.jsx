import { useState } from "react";
import api from "../services/api";

function BugForm() {
  const [bugReport, setBugReport] = useState("");
  const [file, setFile] = useState(null);

  const submitBug = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("bug_report", bugReport);

    if (file) {
      formData.append("file", file);
    }

    try {
      const response = await api.post("/submit", formData);

      console.log("Success:", response.data);

      alert(response.data.message);

      setBugReport("");
      setFile(null);
    } catch (error) {
      console.error("Submission Error:", error);

      if (error.response) {
        console.log("Status Code:", error.response.status);
        console.log("Response Data:", error.response.data);

        alert(
          `Error ${error.response.status}\n\n${JSON.stringify(
            error.response.data,
            null,
            2
          )}`
        );
      } else if (error.request) {
        console.log("No response received:", error.request);

        alert(
          "Backend server se response nahi mila.\n\nCheck karo ki FastAPI server chal raha hai."
        );
      } else {
        console.log("Request Error:", error.message);

        alert(error.message);
      }
    }
  };

  return (
    <div className="container">
      <form onSubmit={submitBug}>
        <textarea
          rows="10"
          placeholder="Paste Bug Report Here..."
          value={bugReport}
          onChange={(e) => setBugReport(e.target.value)}
          required
        />

        <br />
        <br />

        <input
          type="file"
          onChange={(e) => setFile(e.target.files[0])}
        />

        <br />
        <br />

        <button type="submit">
          Submit Bug
        </button>
      </form>
    </div>
  );
}

export default BugForm;