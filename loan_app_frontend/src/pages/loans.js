import axios from "../api/axios";
import IndustrySelect from "../components/IndustrySelect";
import { Navigate } from "react-router-dom";
import React, {useState} from "react";
import Modal from "../components/Modal";
import Notification from "../components/Notification";

export default function Loans() {

    const [redirectToError, setRedirectToError] = useState(false);

    const [isButtonClicked, setIsButtonClicked] = useState(false);

    const [isModalOpen, setIsModalOpen] = useState(false);
    const [isLoanApproved, setIsLoanApproved] = useState(false);

    const [isNotificationOpen, setIsNotificationOpen] = useState(false);
    const [backendError, setBackendError] = useState("");

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
            gross_approval: parseInt(formData.gross_approval),
            term: parseInt(formData.term),
            number_of_employees: parseInt(formData.number_of_employees),
            new_business: formData.new_business === "True" ? parseFloat(1.0.toFixed(1)) : parseFloat(2.0.toFixed(1)),
            urban: formData.location === "Urban" ? 1 : 0,
            industry_name: formData.industry
        });

        console.log("Json form data = ", jsonformData);

        // send form data to the server
        console.log("sending data to the server...");
        try {
            const response = await axios.post(
                '/loans/predict',
                jsonformData
            );

            // handle response
            if (response.status === 200) {
                console.log("Loan application submitted successfully!");
                console.log(response.data);
                // resetFormData();
                // load modal showing success
                setIsLoanApproved(response.data.loan_approved);
                setIsModalOpen(true);
            }
            else if (response.status === 400) {
                // handle bad request error
                console.error("Failed to submit loan application! Check your form data.");
                console.error(response.data)
                // show notification
                setIsNotificationOpen(true);
                setBackendError(response.data.message);
            }
            else if (response.status === 500) {
                // handle server error
                console.error("Server error, please contact support for assistance!");
                console.error(response.data)
            }

        } catch (error) {
            console.error("Error with reaching backend: ", error);
            // // redirect to error page
            console.log("Error response: ", error)
            if (error.message === "Network Error") {
                console.error("Failed to reach the server. Please check your internet connection.");
                // redirect to error page
                setRedirectToError(true);
            }
        }
    }

    // redirect to error page
    if (redirectToError) {
        return <Navigate to="/error" />;
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
        <div className="bg-white h-screen md:h-auto mobile:h-auto static">
             {/*// Modal*/}
            <Modal
                isModalOpen={isModalOpen}
                setIsModalOpen={setIsModalOpen}
                isLoanApproved={isLoanApproved}
            />

            {/*// Main content*/}
            <div
                className="relative h-full isolate overflow-hidden  bg-gradient-to-b from-indigo-500/20 pt-14">
                {/*Notification*/}
                 <Notification
                    isNotificationOpen={isNotificationOpen}
                    setIsNotificationOpen={setIsNotificationOpen}
                    backendError={backendError}
                 />
                <div
                    className="h-full w-full items-center absolute inset-y-0 right-1/2 -z-10 -mr-96
                    origin-top-right skew-x-[-30deg] bg-white shadow-xl shadow-indigo-600/10 ring-1
                     ring-indigo-50 sm:-mr-80 lg:-mr-96"
                    aria-hidden="true"
                />
                    <div
                        className="mx-64 md:mx-12 sm:mx-4 mobile:mx-2 grid grid-cols-1 gap-x-8 gap-y-8 pt-10 md:grid-cols-3"
                    >
                        <div className="px-4 sm:px-0">
                            <h2 className="text-2xl font-extrabold leading-7
                                   bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 bg-clip-text text-transparent"
                            >Loan Application</h2>
                            <p className="mt-1 text-sm leading-6 text-gray-400">Fill in this form to process a loan
                                application. NB: Please provide accurate information.</p>

                            <button className={`flex flex-row items-center content-center mt-12 space-x-2 text-sm
                                                 ${isButtonClicked ? "underline text-purple-800" : "text-gray-400"}`}
                                    onClick={() => setIsButtonClicked(true)}
                                    onPointerLeave={() => setIsButtonClicked(false)}
                            >
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5}
                                     stroke="currentColor" className="w-6 h-6">
                                    <path strokeLinecap="round" strokeLinejoin="round"
                                          d="M6.75 15.75 3 12m0 0 3.75-3.75M3 12h18"
                                    />
                                </svg>
                                go back to home
                            </button>
                        </div>

                        <form
                            onSubmit={handleSubmit}
                            className="bg-white shadow-sm ring-1 ring-gray-900/5 sm:rounded-xl md:col-span-2"
                        >
                            <div className="px-4 py-6 sm:p-8">
                                <div className="grid max-w-2xl grid-cols-1 gap-x-6 gap-y-8 sm:grid-cols-6">
                                {/*Company name*/}
                                    <div className="sm:col-span-3">
                                        <label htmlFor="company_name"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            Company name
                                        </label>
                                        <div className="mt-2">
                                            <input
                                                type="text"
                                                name="company_name"
                                                id="company_name"
                                                value={formData.company_name}
                                                onChange={handleChange}
                                                autoComplete="given-name"
                                                className="block w-full rounded-md border-0 py-1.5 text-gray-900 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                                            />
                                        </div>
                                    </div>
                                    {/*Gross approval*/}
                                    <div className="sm:col-span-3">
                                        <label htmlFor="gross_approval"
                                               className="block text-sm font-medium leading-6 text-gray-900">
                                            Gross approval
                                            <span className="text-gray-400"> (in USD)</span>
                                        </label>
                                        <div className="mt-2">
                                            <input
                                                type="Number"
                                                name="gross_approval"
                                                id="gross_approval"
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

