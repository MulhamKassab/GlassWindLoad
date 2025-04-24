export default function ResultsPanel({ result }) {
    if (!result) return null;
  
    return (
      <div className="mt-8 border p-4 rounded-lg bg-green-50">
        <h3 className="text-lg font-semibold mb-2">Results</h3>
        <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(result.lr_result, null, 2)}</pre>
        <pre className="text-sm whitespace-pre-wrap">{JSON.stringify(result.cof, null, 2)}</pre>
  
        {result.pdf_url && (
          <a
            href={result.pdf_url}
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-700 underline mt-4 inline-block"
          >
            Download PDF report
          </a>
        )}
      </div>
    );
  }
  