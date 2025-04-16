// src/components/UserDropdown.jsx
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";
import { ChevronDownIcon } from "@heroicons/react/20/solid";
import { useAuth } from "../context/AuthContext";

export default function UserDropdown() {
    const { user, logout } = useAuth();

    return (
        <Menu as="div" className="relative inline-block text-left">
        <MenuButton className="inline-flex items-center gap-2 rounded-md bg-white px-3 py-2 text-sm font-medium text-gray-900 shadow-xs ring-1 ring-gray-300 hover:bg-gray-50">
            <img
            src={user.picture}
            alt="Profil"
            className="w-6 h-6 rounded-full"
            />
            {user.name}
            <ChevronDownIcon className="w-4 h-4 text-gray-400" />
        </MenuButton>

        <MenuItems
            transition
            className="absolute right-0 z-10 mt-2 w-48 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black/5 focus:outline-none"
        >
            <div className="py-1">
            <MenuItem>
                {({ active }) => (
                <button
                    onClick={logout}
                    className={`${
                    active ? 'bg-gray-100 text-gray-900' : 'text-gray-700'
                    } block w-full px-4 py-2 text-sm text-left`}
                >
                    Log ud
                </button>
                )}
            </MenuItem>
            </div>
        </MenuItems>
        </Menu>
    )
}