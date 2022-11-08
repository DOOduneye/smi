import Button from "./Button"

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagnifyingGlass } from '@fortawesome/free-solid-svg-icons'

const Input = () => {
    return (
        <label className="flex flex-row border border-slate-300 rounded-md">
            <span className="sr-only">Search</span>
            <span className="relative inset-y-0 left-3 flex items-center">
                <FontAwesomeIcon icon={faMagnifyingGlass} className="text-slate-400" />
            </span>
            <input className="placeholder:italic placeholder:text-slate-400 text-slate-500 flex bg-white w-full py-2 pl-6 pr-3 shadow-sm focus:outline-none focus:border-sky-500 focus:ring-sky-500 sm:text-sm" placeholder="Search for songs..." type="text" name="search"/>
            <Button />
        </label>
    )
}

export default Input

