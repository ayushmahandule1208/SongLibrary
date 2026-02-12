import React, { useState } from 'react';
import { Download, Check } from 'lucide-react';
import { exportToCSV } from '../utils/csvExport';
import './CSVDownload.css';

const CSVDownload = ({ data, filename = 'songs_data.csv' }) => {
  const [downloaded, setDownloaded] = useState(false);

  const handleDownload = () => {
    if (!data || data.length === 0) {
      alert('No data available to download');
      return;
    }

    exportToCSV(data, filename);
    setDownloaded(true);

    setTimeout(() => {
      setDownloaded(false);
    }, 2000);
  };

  return (
    <button
      className={`csv-download-button ${downloaded ? 'downloaded' : ''}`}
      onClick={handleDownload}
      disabled={!data || data.length === 0}
    >
      {downloaded ? (
        <>
          <Check size={20} />
          <span>Downloaded!</span>
        </>
      ) : (
        <>
          <Download size={20} />
          <span>Export CSV</span>
        </>
      )}
    </button>
  );
};

export default CSVDownload;