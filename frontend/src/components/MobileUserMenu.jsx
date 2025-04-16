import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/react";
import { ChevronDownIcon } from "@heroicons/react/20/solid";
import { useAuth } from "../context/AuthContext";

export default function MobileUserMenu() {
    const { user, logout } = useAuth()
  
    return (
      <Menu as="div" className="w-full px-3">
        <MenuButton className="flex items-center justify-between w-full py-2.5 rounded-md bg-gray-100 px-4 text-sm font-medium text-gray-900">
          <div className="flex items-center gap-2">
            <img src={user.picture} alt="profil" className="w-8 h-8 rounded-full" />
            {user.name}
          </div>
          <ChevronDownIcon className="w-5 h-5 text-gray-500" />
        </MenuButton>
  
        <MenuItems className="mt-2 w-full rounded-md bg-white shadow-md ring-1 ring-black/5">
          <MenuItem>
            {({ active }) => (
              <button
                onClick={logout}
                className={`${
                  active ? 'bg-gray-100' : ''
                } block w-full text-left px-4 py-2 text-sm text-gray-700`}
              >
                Log ud
              </button>
            )}
          </MenuItem>
        </MenuItems>
      </Menu>
    )
  }