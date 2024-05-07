import React from 'react';

// Unique industries as a list
const uniqueIndustries = [
  'Agriculture, forestry, fishing, hunting',
  'Mining, quarrying, oil and gas extraction',
  'Utilities',
  'Construction',
  'Manufacturing',
  'Wholesale_trade',
  'Retail_trade',
  'Transportation, warehousing',
  'Information',
  'Finance, Insurance',
  'Real estate, rental, leasing',
  'Professional, scientific, technical services',
  'Management of companies, enterprises',
  'Administrative support, waste management',
  'Educational',
  'Healthcare, Social_assist',
  'Arts, Entertain, recreation',
  'Accomodation, Food services',
  'Other services',
  'Public adminstration',
];

export default function IndustrySelect ({ selectedIndustry, onIndustryChange }) {
    return (
        <div className="sm:col-span-3">
            <label htmlFor="industry" className="block text-sm font-medium text-gray-900">
                Industry
            </label>
            <div className="mt-2">
                <select
                    id="industry"
                    name="industry"
                    value={selectedIndustry} // Ensure this is properly managed by parent
                    onChange={onIndustryChange} // Pass the event to parent
                    className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                >
                    <option value="">Select Industry</option>
                    {uniqueIndustries.map((industry, index) => (
                        <option key={index} value={industry}>
                            {industry}
                        </option>
                    ))}
                </select>
            </div>
        </div>
    );
}

