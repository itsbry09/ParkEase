import tkinter as tk
from tkinter import ttk, messagebox
import json

class MallParkApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MallPark - Parking System")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f8f9fa')
        
        # Session data (simulating user login)
        self.session = {
            'user_id': None,
            'username': None,
            'user_type': None  # 'admin' or 'staff'
        }
        
        # Set up the main container
        self.main_container = tk.Frame(root, bg='#f8f9fa')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        # Initialize UI
        self.create_navbar()
        self.create_content_area()
        
        # Show login screen initially
        self.show_login_screen()
    
    def create_navbar(self):
        # Navbar frame
        self.navbar = tk.Frame(
            self.main_container,
            bg='#343a40',
            height=60
        )
        self.navbar.pack(fill=tk.X, side=tk.TOP)
        self.navbar.pack_propagate(False)
        
        # Brand/logo
        self.brand_frame = tk.Frame(self.navbar, bg='#343a40')
        self.brand_frame.pack(side=tk.LEFT, padx=20, pady=15)
        
        self.brand_icon = tk.Label(
            self.brand_frame,
            text="Ⓟ",
            bg='#343a40',
            fg='white',
            font=('Arial', 16, 'bold')
        )
        self.brand_icon.pack(side=tk.LEFT)
        
        self.brand_text = tk.Label(
            self.brand_frame,
            text="MallPark",
            bg='#343a40',
            fg='white',
            font=('Arial', 18, 'bold')
        )
        self.brand_text.pack(side=tk.LEFT, padx=(5, 0))
        
        # Navigation items (initially empty, populated after login)
        self.nav_items_frame = tk.Frame(self.navbar, bg='#343a40')
        self.nav_items_frame.pack(side=tk.RIGHT, padx=20, pady=15)
    
    def create_content_area(self):
        # Content area for different pages
        self.content_area = tk.Frame(
            self.main_container,
            bg='#f8f9fa',
            padx=20,
            pady=20
        )
        self.content_area.pack(fill=tk.BOTH, expand=True)
    
    def show_login_screen(self):
        # Clear content area
        for widget in self.content_area.winfo_children():
            widget.destroy()
        
        # Clear navbar items
        for widget in self.nav_items_frame.winfo_children():
            widget.destroy()
        
        # Login form
        login_frame = tk.Frame(
            self.content_area,
            bg='white',
            padx=40,
            pady=40,
            relief=tk.RAISED,
            bd=1
        )
        login_frame.pack(expand=True)
        
        tk.Label(
            login_frame,
            text="MallPark Login",
            bg='white',
            fg='#343a40',
            font=('Arial', 24, 'bold')
        ).pack(pady=(0, 30))
        
        # Username
        tk.Label(
            login_frame,
            text="Username:",
            bg='white',
            font=('Arial', 12),
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        username_entry = tk.Entry(
            login_frame,
            font=('Arial', 12),
            width=30
        )
        username_entry.pack(pady=(0, 15))
        
        # Password
        tk.Label(
            login_frame,
            text="Password:",
            bg='white',
            font=('Arial', 12),
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        password_entry = tk.Entry(
            login_frame,
            font=('Arial', 12),
            width=30,
            show="•"
        )
        password_entry.pack(pady=(0, 20))
        
        # User type
        user_type_frame = tk.Frame(login_frame, bg='white')
        user_type_frame.pack(fill=tk.X, pady=(0, 20))
        
        tk.Label(
            user_type_frame,
            text="Login as:",
            bg='white',
            font=('Arial', 12)
        ).pack(side=tk.LEFT)
        
        user_type_var = tk.StringVar(value="staff")
        tk.Radiobutton(
            user_type_frame,
            text="Staff",
            variable=user_type_var,
            value="staff",
            bg='white'
        ).pack(side=tk.LEFT, padx=(20, 10))
        
        tk.Radiobutton(
            user_type_frame,
            text="Admin",
            variable=user_type_var,
            value="admin",
            bg='white'
        ).pack(side=tk.LEFT)
        
        # Login button
        def perform_login():
            username = username_entry.get()
            password = password_entry.get()
            user_type = user_type_var.get()
            
            if username and password:
                self.session = {
                    'user_id': 1,
                    'username': username,
                    'user_type': user_type
                }
                self.update_navbar()
                self.show_dashboard()
            else:
                messagebox.showerror("Error", "Please enter username and password")
        
        login_btn = tk.Button(
            login_frame,
            text="Login",
            bg='#007bff',
            fg='white',
            font=('Arial', 12, 'bold'),
            command=perform_login,
            width=20,
            height=2
        )
        login_btn.pack(pady=(10, 0))
    
    def update_navbar(self):
        # Clear existing navbar items
        for widget in self.nav_items_frame.winfo_children():
            widget.destroy()
        
        if self.session['user_id']:
            # User badge
            badge_color = '#dc3545' if self.session['user_type'] == 'admin' else '#0d6efd'
            user_badge = tk.Label(
                self.nav_items_frame,
                text=f" {self.session['username']} ({self.session['user_type']}) ",
                bg=badge_color,
                fg='white',
                font=('Arial', 10, 'bold'),
                relief=tk.RAISED,
                bd=1
            )
            user_badge.pack(side=tk.LEFT, padx=(0, 15))
            
            # Navigation buttons
            nav_buttons = [
                ("Dashboard", self.show_dashboard),
                ("Slots", self.show_slots),
                ("History", self.show_history)
            ]
            
            if self.session['user_type'] == 'admin':
                nav_buttons.extend([
                    ("Manage Staff", self.manage_staff),
                    ("Reports", self.show_reports)
                ])
            else:
                nav_buttons.append(("Park Vehicle", self.park_vehicle))
            
            # Add navigation buttons
            for text, command in nav_buttons:
                btn = tk.Button(
                    self.nav_items_frame,
                    text=text,
                    bg='#343a40',
                    fg='white',
                    font=('Arial', 10),
                    relief=tk.FLAT,
                    command=command
                )
                btn.pack(side=tk.LEFT, padx=5)
            
            # Logout button
            logout_btn = tk.Button(
                self.nav_items_frame,
                text="Logout",
                bg='#6c757d',
                fg='white',
                font=('Arial', 10),
                relief=tk.FLAT,
                command=self.logout
            )
            logout_btn.pack(side=tk.LEFT, padx=(15, 0))
    
    def show_dashboard(self):
        self.clear_content_area()
        
        tk.Label(
            self.content_area,
            text="Dashboard",
            bg='#f8f9fa',
            fg='#343a40',
            font=('Arial', 24, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Dashboard content
        stats_frame = tk.Frame(self.content_area, bg='#f8f9fa')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Statistics cards
        stats = [
            ("Total Slots", "150", "#007bff"),
            ("Occupied", "87", "#dc3545"),
            ("Available", "63", "#28a745"),
            ("Today's Revenue", "$1,240", "#ffc107")
        ]
        
        for i, (title, value, color) in enumerate(stats):
            card = tk.Frame(
                stats_frame,
                bg=color,
                relief=tk.RAISED,
                bd=1,
                width=200,
                height=100
            )
            card.pack(side=tk.LEFT, padx=(0, 15))
            card.pack_propagate(False)
            
            tk.Label(
                card,
                text=title,
                bg=color,
                fg='white',
                font=('Arial', 12)
            ).pack(pady=(15, 5))
            
            tk.Label(
                card,
                text=value,
                bg=color,
                fg='white',
                font=('Arial', 18, 'bold')
            ).pack()
        
        # Recent activity
        activity_frame = tk.Frame(self.content_area, bg='white', relief=tk.RAISED, bd=1)
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        tk.Label(
            activity_frame,
            text="Recent Activity",
            bg='white',
            fg='#343a40',
            font=('Arial', 16, 'bold')
        ).pack(anchor=tk.W, padx=20, pady=15)
        
        # Sample activity data
        activities = [
            ("ABC123", "Parked", "Level 1 - A12", "2 hours ago"),
            ("XYZ789", "Exited", "Level 2 - B05", "1 hour ago"),
            ("DEF456", "Parked", "Level 1 - A08", "45 minutes ago")
        ]
        
        for vehicle, action, location, time in activities:
            activity_item = tk.Frame(activity_frame, bg='white')
            activity_item.pack(fill=tk.X, padx=20, pady=5)
            
            tk.Label(
                activity_item,
                text=f"{vehicle} - {action} at {location}",
                bg='white',
                font=('Arial', 11)
            ).pack(side=tk.LEFT)
            
            tk.Label(
                activity_item,
                text=time,
                bg='white',
                fg='#6c757d',
                font=('Arial', 10)
            ).pack(side=tk.RIGHT)
    
    def show_slots(self):
        self.clear_content_area()
        
        tk.Label(
            self.content_area,
            text="Parking Slots",
            bg='#f8f9fa',
            fg='#343a40',
            font=('Arial', 24, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Slot status
        status_frame = tk.Frame(self.content_area, bg='#f8f9fa')
        status_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Create sample parking slots visualization
        slots_frame = tk.Frame(self.content_area, bg='#f8f9fa')
        slots_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sample slots data
        levels = [
            ("Level 1", 20, 8),
            ("Level 2", 25, 15),
            ("Level 3", 30, 22)
        ]
        
        for level_name, total_slots, occupied in levels:
            level_frame = tk.Frame(slots_frame, bg='white', relief=tk.RAISED, bd=1)
            level_frame.pack(fill=tk.X, pady=(0, 15))
            
            # Level header
            header_frame = tk.Frame(level_frame, bg='#e9ecef')
            header_frame.pack(fill=tk.X)
            
            tk.Label(
                header_frame,
                text=f"{level_name} ({occupied}/{total_slots} occupied)",
                bg='#e9ecef',
                fg='#343a40',
                font=('Arial', 14, 'bold'),
                padx=15,
                pady=10
            ).pack(anchor=tk.W)
            
            # Slots visualization
            slots_container = tk.Frame(level_frame, bg='white', padx=15, pady=15)
            slots_container.pack(fill=tk.X)
            
            # Create slot indicators
            for i in range(total_slots):
                slot_color = '#dc3545' if i < occupied else '#28a745'
                slot = tk.Frame(
                    slots_container,
                    bg=slot_color,
                    width=40,
                    height=40,
                    relief=tk.RAISED,
                    bd=1
                )
                slot.pack(side=tk.LEFT, padx=2, pady=2)
                slot.pack_propagate(False)
                
                tk.Label(
                    slot,
                    text=str(i+1),
                    bg=slot_color,
                    fg='white',
                    font=('Arial', 8, 'bold')
                ).pack(expand=True)
    
    def show_history(self):
        self.clear_content_area()
        
        tk.Label(
            self.content_area,
            text="Parking History",
            bg='#f8f9fa',
            fg='#343a40',
            font=('Arial', 24, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # History table
        history_frame = tk.Frame(self.content_area, bg='white', relief=tk.RAISED, bd=1)
        history_frame.pack(fill=tk.BOTH, expand=True)
        
        # Table headers
        headers = ["Vehicle", "Entry Time", "Exit Time", "Duration", "Slot", "Amount"]
        header_frame = tk.Frame(history_frame, bg='#343a40')
        header_frame.pack(fill=tk.X)
        
        for i, header in enumerate(headers):
            tk.Label(
                header_frame,
                text=header,
                bg='#343a40',
                fg='white',
                font=('Arial', 12, 'bold'),
                padx=10,
                pady=10
            ).grid(row=0, column=i, sticky='ew')
            header_frame.columnconfigure(i, weight=1)
        
        # Sample history data
        history_data = [
            ("ABC123", "10:30 AM", "2:45 PM", "4h 15m", "A12", "$12.50"),
            ("XYZ789", "9:15 AM", "1:30 PM", "4h 15m", "B05", "$12.50"),
            ("DEF456", "11:00 AM", "3:20 PM", "4h 20m", "A08", "$13.00")
        ]
        
        for row, data in enumerate(history_data):
            row_frame = tk.Frame(history_frame, bg='white' if row % 2 == 0 else '#f8f9fa')
            row_frame.pack(fill=tk.X)
            
            for col, value in enumerate(data):
                tk.Label(
                    row_frame,
                    text=value,
                    bg=row_frame['bg'],
                    font=('Arial', 11),
                    padx=10,
                    pady=8
                ).grid(row=0, column=col, sticky='ew')
                row_frame.columnconfigure(col, weight=1)
    
    def manage_staff(self):
        if self.session['user_type'] != 'admin':
            messagebox.showerror("Access Denied", "Admin access required")
            return
        
        self.clear_content_area()
        
        tk.Label(
            self.content_area,
            text="Manage Staff",
            bg='#f8f9fa',
            fg='#343a40',
            font=('Arial', 24, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Staff management content
        staff_frame = tk.Frame(self.content_area, bg='white', relief=tk.RAISED, bd=1)
        staff_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        tk.Label(
            staff_frame,
            text="Staff Members",
            bg='white',
            fg='#343a40',
            font=('Arial', 16, 'bold')
        ).pack(anchor=tk.W, padx=20, pady=15)
        
        # Sample staff data
        staff_data = [
            ("john_doe", "John Doe", "Active"),
            ("jane_smith", "Jane Smith", "Active"),
            ("bob_wilson", "Bob Wilson", "Inactive")
        ]
        
        for username, name, status in staff_data:
            staff_item = tk.Frame(staff_frame, bg='white')
            staff_item.pack(fill=tk.X, padx=20, pady=8)
            
            tk.Label(
                staff_item,
                text=f"{name} ({username})",
                bg='white',
                font=('Arial', 12)
            ).pack(side=tk.LEFT)
            
            status_color = '#28a745' if status == 'Active' else '#dc3545'
            status_label = tk.Label(
                staff_item,
                text=status,
                bg=status_color,
                fg='white',
                font=('Arial', 10, 'bold'),
                padx=10,
                pady=2
            )
            status_label.pack(side=tk.RIGHT, padx=(0, 10))
            
            # Action buttons
            actions_frame = tk.Frame(staff_item, bg='white')
            actions_frame.pack(side=tk.RIGHT)
            
            tk.Button(
                actions_frame,
                text="Edit",
                bg='#ffc107',
                fg='#343a40',
                font=('Arial', 9),
                width=8
            ).pack(side=tk.LEFT, padx=2)
            
            tk.Button(
                actions_frame,
                text="Delete",
                bg='#dc3545',
                fg='white',
                font=('Arial', 9),
                width=8
            ).pack(side=tk.LEFT, padx=2)
    
    def show_reports(self):
        if self.session['user_type'] != 'admin':
            messagebox.showerror("Access Denied", "Admin access required")
            return
        
        self.clear_content_area()
        
        tk.Label(
            self.content_area,
            text="Reports",
            bg='#f8f9fa',
            fg='#343a40',
            font=('Arial', 24, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Reports content
        reports_frame = tk.Frame(self.content_area, bg='white', relief=tk.RAISED, bd=1)
        reports_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        tk.Label(
            reports_frame,
            text="System Reports",
            bg='white',
            fg='#343a40',
            font=('Arial', 16, 'bold')
        ).pack(anchor=tk.W, padx=20, pady=15)
        
        # Report options
        report_types = [
            "Daily Revenue Report",
            "Monthly Occupancy Report", 
            "Vehicle Type Analysis",
            "Peak Hours Analysis",
            "Staff Performance Report"
        ]
        
        for report in report_types:
            report_item = tk.Frame(reports_frame, bg='white')
            report_item.pack(fill=tk.X, padx=20, pady=8)
            
            tk.Label(
                report_item,
                text=report,
                bg='white',
                font=('Arial', 12)
            ).pack(side=tk.LEFT)
            
            tk.Button(
                report_item,
                text="Generate",
                bg='#007bff',
                fg='white',
                font=('Arial', 10),
                width=10
            ).pack(side=tk.RIGHT)
    
    def park_vehicle(self):
        if self.session['user_type'] != 'staff':
            messagebox.showerror("Access Denied", "Staff access required")
            return
        
        self.clear_content_area()
        
        tk.Label(
            self.content_area,
            text="Park Vehicle",
            bg='#f8f9fa',
            fg='#343a40',
            font=('Arial', 24, 'bold')
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Park vehicle form
        form_frame = tk.Frame(self.content_area, bg='white', relief=tk.RAISED, bd=1, padx=30, pady=30)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Vehicle number
        tk.Label(
            form_frame,
            text="Vehicle Number:",
            bg='white',
            font=('Arial', 12),
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        vehicle_entry = tk.Entry(
            form_frame,
            font=('Arial', 12),
            width=30
        )
        vehicle_entry.pack(fill=tk.X, pady=(0, 15))
        
        # Vehicle type
        type_frame = tk.Frame(form_frame, bg='white')
        type_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(
            type_frame,
            text="Vehicle Type:",
            bg='white',
            font=('Arial', 12)
        ).pack(side=tk.LEFT)
        
        vehicle_type = tk.StringVar(value="car")
        types = [("Car", "car"), ("Motorcycle", "motorcycle"), ("Truck", "truck")]
        
        for text, value in types:
            tk.Radiobutton(
                type_frame,
                text=text,
                variable=vehicle_type,
                value=value,
                bg='white'
            ).pack(side=tk.LEFT, padx=(20, 10))
        
        # Available slots
        tk.Label(
            form_frame,
            text="Available Slots:",
            bg='white',
            font=('Arial', 12),
            anchor=tk.W
        ).pack(fill=tk.X, pady=(0, 5))
        
        # Sample available slots
        slots_frame = tk.Frame(form_frame, bg='white')
        slots_frame.pack(fill=tk.X, pady=(0, 20))
        
        available_slots = ["A05", "A12", "B03", "B08", "C01"]
        slot_var = tk.StringVar(value=available_slots[0])
        
        for slot in available_slots:
            tk.Radiobutton(
                slots_frame,
                text=slot,
                variable=slot_var,
                value=slot,
                bg='white'
            ).pack(side=tk.LEFT, padx=(0, 15))
        
        # Park button
        def park_vehicle():
            vehicle_no = vehicle_entry.get()
            if vehicle_no:
                messagebox.showinfo("Success", f"Vehicle {vehicle_no} parked at {slot_var.get()}")
            else:
                messagebox.showerror("Error", "Please enter vehicle number")
        
        park_btn = tk.Button(
            form_frame,
            text="Park Vehicle",
            bg='#28a745',
            fg='white',
            font=('Arial', 12, 'bold'),
            command=park_vehicle,
            width=20,
            height=2
        )
        park_btn.pack(pady=(20, 0))
    
    def clear_content_area(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()
    
    def logout(self):
        self.session = {'user_id': None, 'username': None, 'user_type': None}
        self.show_login_screen()

if __name__ == "__main__":
    root = tk.Tk()
    app = MallParkApp(root)
    root.mainloop()