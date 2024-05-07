import axios from "../api/axios";
import IndustrySelect from "../components/IndustrySelect";
import React from "react";

export default function Loans() {

    const [formData, setFormData] = React.useState({
        company_name: "",
        gross_approval: "",
        location: "",
        industry: "",
        term: "",
        number_of_employees: "",
        new_business: ""
    });

    // handle formData changes
    const handleChange = (e) => {
        const { name, value } = e.target;

        setFormData((prevData) => ({
        ...prevData,
        [name]: value,
        }));
    };


    // handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault(); // prevent default form submission

        // log
        console.log("formData before transformation = ", formData);

        // transform form data to JSON
        const jsonformData = JSON.stringify({
            company_name: formData.company_name,
            gross_approval: formData.gross_approval,
            term: formData.term,
            number_of_employees: formData.number_of_employees,
            new_business: formData.new_business === "True" ? 1.0 : 2.0,
            urban: formData.location === "Urban" ? 1 : 0,
            industry: formData.industry
        });

        console.log("Json form data = ", jsonformData);

        // send form data to the server
        console.log("sending data to the server...");
        try {
            const response = await axios.post(
                '/loans/predict',
                formData
            );

            // handle response
            if (response.status === 200) {
                console.log("Loan application submitted successfully!");
                console.log(response);
                resetFormData();
            }
            else {
                console.error("Failed to submit loan application!");
            }

        } catch (error) {
            console.error("Error: ", error);
        }
    }

    // reset form data
    const resetFormData = () => {
        setFormData({
            company_name: "",
            gross_approval: "",
            location: "",
            industry: "",
            term: "",
            number_of_employees: "",
            new_business: ""
        });
    }

    return (
        <div className="bg-white h-screen">
            <div className="relative h-full isolate overflow-hidden  bg-gradient-to-b from-indigo-500/20 pt-14">
                <div
                    className="w-full h absolute inset-y-0 right-1/2 -z-10 -mr-96
                    origin-top-right skew-x-[-30deg] bg-white shadow-xl shadow-indigo-600/10 ring-1 ring-indigo-50 sm:-mr-80 lg:-mr-96"
                    aria-hidden="true"
                />
                    <div className="mx-64 grid grid-cols-1 gap-x-8 gap-y-8 pt-10 md:grid-cols-3">
                        <div className="px-4 sm:px-0">
                            <h2 className="text-2xl font-extrabold leading-7
                               bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text text-transparent"
                            >Loan Application</h2>
                            <p className="mt-1 text-sm leading-6 text-gray-400">Fill in this form to process a loan
                                application. NB: Please provide accurate information.</p>
                        </div>

                        <form
                            onSubmit={handleSubmit}
                            className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2"
                        >
                            <div className="px-4 py-6 sm:p-8">
                                <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                                    {/*Company name*/}
                                    <div className="sm:col-span-3">
                                        <label htmlFor="company-name"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            Company name
                                        </label>
                                        <div className="mt-2">
                                            <input
                                                type="text"
                                                name="company-name"
                                                id="compay-name"
                                                value={formData.company_name}
                                                onChange={handleChange}
                                                autoComplete="given-name"
                                                className="block w-full rounded-md border-0 py-1.5 text-gray-900
                                                 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400
                                                  focus:ring-2 focus:ring-inset focus:ring-pink-400 sm:text-sm
                                                   sm:leading-6"
                                            />
                                        </div>
                                    </div>

                                    {/*Gross approval*/}

                                    <div className="sm:col-span-3">
                                        <label htmlFor="gross-approval"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            Gross approval
                                            <span className="text-gray-400"> (in USD)</span>
                                        </label>
                                        <div className="mt-2">
                                            <input
                                                type="Number"
                                                name="gross-approval"
                                                id="gross-approval"
                                                value={formData.gross_approval}
                                                onChange={handleChange}
                                                autoComplete=""
                                                className="block w-full rounded-md border-0 py-1.5 text-gray-900
                                                 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400
                                                 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm
                                                 sm:leading-6"
                                            />
                                        </div>
                                    </div>

                                    {/*Urban or Rural */}

                                    <div className="sm:col-span-3">
                                        <label htmlFor="location"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            Location
                                            <span className="text-gray-400"> (Urban or Rural?)</span>
                                        </label>
                                        <div className="mt-2">
                                            <select
                                                id="location"
                                                name="location"
                                                value={formData.location}
                                                onChange={handleChange}
                                                autoComplete=""
                                                className="block w-1/2 rounded-md border-0 py-1.5 text-gray-900
                                                shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset
                                                focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6"
                                            >
                                                <option value="">Select Location</option>
                                                <option>Urban</option>
                                                <option>Rural</option>
                                            </select>
                                        </div>
                                    </div>

                                    {/*industry*/}

                                    <IndustrySelect
                                          selectedIndustry={formData.industry}
                                          onIndustryChange={(e) => {
                                            if (e && e.target) {
                                              handleChange({
                                                target: {
                                                  name: 'industry',
                                                  value: e.target.value,
                                                },
                                              });
                                            }
                                          }}
                                    />

                                    {/*Term*/}


                                    <div className="sm:col-span-4">
                                        <label htmlFor="term"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            Term
                                            <span className="text-gray-400"> (in months)</span>
                                        </label>
                                        <div className="mt-2">
                                            <input
                                                id="term"
                                                name="term"
                                                type="Number"
                                                value={formData.term}
                                                onChange={handleChange}
                                                autoComplete=""
                                                className="block w-full rounded-md border-0 py-1.5 text-gray-900
                                                 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400
                                                 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm
                                                 sm:leading-6"
                                            />
                                        </div>
                                    </div>

                                    {/*Number of employees*/}

                                    <div className="sm:col-span-4">
                                        <label htmlFor="number_of_employees"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            Number of employees
                                            <span className="text-gray-400"> (e.g 350)</span>
                                        </label>
                                        <div className="mt-2">
                                            <input
                                                id="number_of_employees"
                                                name="number_of_employees"
                                                type="Number"
                                                value={formData.number_of_employees}
                                                onChange={handleChange}
                                                autoComplete=""
                                                className="block w-full rounded-md border-0 py-1.5 text-gray-900
                                                shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400
                                                 focus:ring-2 focus:ring-inset focus:ring-indigo-600
                                                 sm:text-sm sm:leading-6"
                                            />
                                        </div>
                                    </div>

                                    {/* New business */}


                                    <div className="sm:col-span-4">
                                        <label htmlFor="new_business"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            New business
                                            <span className="text-gray-400"> (Is it a new business or not?)</span>
                                        </label>
                                        <div className="mt-2">
                                            <select
                                                id="new_business"
                                                name="new_business"
                                                value={formData.new_business}
                                                onChange={handleChange}
                                                autoComplete=""
                                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:max-w-xs sm:text-sm sm:leading-6"
                                            >
                                                <option value="">Select</option>
                                                <option>True</option>
                                                <option>False</option>
                                            </select>
                                        </div>
                                    </div>

                                </div>
                            </div>

                            {/*Form submission */}
                            <div
                                className="flex items-center justify-end gap-x-6 border-t border-gray-900/10 px-4 py-4 sm:px-8">
                                <button type="button" className="text-sm font-semibold leading-6 text-gray-900"
                                        onClick={resetFormData}
                                >
                                    Cancel
                                </button>
                                <button
                                    type="submit"
                                    className="self-center rounded-full align-middle bg-gradient-to-r from-indigo-600
                                    to-pink-500 px-5 py-3 text-sm font-semibold text-white shadow-sm drop-shadow-md
                                    hover:drop-shadow-2xl focus-visible:outline focus-visible:outline-2
                                    focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
                                >
                                    Submit
                                </button>
                            </div>
                        </form>
                    </div>
            </div>
        </div>
    )
}

