from manim import *
import numpy as np

np.random.seed(42)

class NavierStokesEq(Scene):
    def construct(self):
        title = Title("Navier-Stokes equations")
        self.play(Write(title))
        eq = MathTex(
            r"""
            \frac{\partial u}{\partial t} &= -(u \cdot \nabla) u+\nu \nabla^2 u+\mathbf{f} \\
            \frac{\partial \rho}{\partial t} &= -(u \cdot \nabla) \rho+\kappa \nabla^2 \rho + S
            """,
        ).scale(1).move_to(ORIGIN)
        self.play(Write(eq))
        self.wait(2)

class VelEqBreakdown(Scene):
    def construct(self):
        # Create the full equation
        eq = MathTex(
            r"\frac{\partial u}{\partial t}", 
            r"=", 
            r"-(u \cdot \nabla) u",
            r"+",
            r"\nu \nabla^2 u",
            r"+",
            r"\mathbf{f}"
        ).scale(1.5).move_to(ORIGIN)
        
        # Create explanations for each term
        explanations = [
            "Time derivative of velocity",
            "Advection term",
            "Diffusion term",
            "External forces"
        ]
        
        # Create explanation text
        explanation = Text("", font_size=36).to_edge(DOWN, buff=1)
        
        # Show the full equation
        self.play(Write(eq))
        self.wait(1)
        
        # Define term indices to highlight
        term_indices = [0, 2, 4, 6]  # Indices of the terms in the eq object
        
        # Create an empty highlight box
        highlight_box = None
        
        for i, idx in enumerate(term_indices):
            # Get the part to highlight
            part = eq[idx]
            
            # Create a highlight box around the term
            new_box = SurroundingRectangle(part, buff=0.1, color=YELLOW)
            
            # Animate highlight box and explanation
            if highlight_box is None:
                self.play(
                    Create(new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            else:
                self.play(
                    ReplacementTransform(highlight_box, new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            
            # Update the highlight box reference
            highlight_box = new_box
            
            self.wait(2)
        
        # Remove the final highlight box
        self.play(
            FadeOut(highlight_box),
            explanation.animate.become(Text("", font_size=36).to_edge(DOWN, buff=1))
        )
        
        # Final pause
        self.wait(2)

class DensityEqBreakdown(Scene):
    def construct(self):
        # Create the full equation
        eq = MathTex(
            r"\frac{\partial \rho}{\partial t}", 
            r"=", 
            r"-(u \cdot \nabla) \rho",
            r"+",
            r"\kappa \nabla^2 \rho",
            r"+",
            r"S"
        ).scale(1.5).move_to(ORIGIN)
        
        # Create explanations for each term
        explanations = [
            "Time derivative of density",
            "Advection term",
            "Diffusion term",
            "External sources"
        ]
        
        # Create explanation text
        explanation = Text("", font_size=36).to_edge(DOWN, buff=1)
        
        # Show the full equation
        self.play(Write(eq))
        self.wait(1)
        
        # Define term indices to highlight
        term_indices = [0, 2, 4, 6]  # Indices of the terms in the eq object
        
        # Create an empty highlight box
        highlight_box = None
        
        for i, idx in enumerate(term_indices):
            # Get the part to highlight
            part = eq[idx]
            
            # Create a highlight box around the term
            new_box = SurroundingRectangle(part, buff=0.1, color=YELLOW)
            
            # Animate highlight box and explanation
            if highlight_box is None:
                self.play(
                    Create(new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            else:
                self.play(
                    ReplacementTransform(highlight_box, new_box),
                    explanation.animate.become(Text(explanations[i], font_size=36).to_edge(DOWN, buff=1))
                )
            
            # Update the highlight box reference
            highlight_box = new_box
            
            self.wait(2)
        
        # Remove the final highlight box
        self.play(
            FadeOut(highlight_box),
            explanation.animate.become(Text("", font_size=36).to_edge(DOWN, buff=1))
        )
        
        # Final pause
        self.wait(2)

class GridAnimation(Scene):
    def construct(self):
        # Parameters
        N = 5  # This means we'll have an (N+1)×(N+1) grid (from 0 to N+1)
        cell_size = 0.8
        grid_width = (N + 2) * cell_size
        grid_height = (N + 2) * cell_size
        
        # Create grid
        grid = VGroup()
        
        # Create horizontal and vertical lines
        for i in range(N + 3):  # 0 to N+2 lines
            # Horizontal line
            h_line = Line(
                start=[-grid_width/2, -grid_height/2 + i * cell_size, 0],
                end=[grid_width/2, -grid_height/2 + i * cell_size, 0],
                stroke_width=2,
            )
            grid.add(h_line)
            
            # Vertical line
            v_line = Line(
                start=[-grid_width/2 + i * cell_size, -grid_height/2, 0],
                end=[-grid_width/2 + i * cell_size, grid_height/2, 0],
                stroke_width=2,
            )
            grid.add(v_line)
        
        # Position grid on the left side
        grid.move_to(LEFT * 3)
        
        # Add labels for rows and columns
        labels = VGroup()
        
        # Define symbolic labels
        symbolic_labels = ["0", "1", "2", r"\ldots", "N", "N+1"]
        
        # Column labels (x-axis)
        for i in range(N + 2):  # 0 to N+1
            # Choose the appropriate label
            if i == 0:
                label_text = symbolic_labels[0]  # 0
            elif i == 1:
                label_text = symbolic_labels[1]  # 1
            elif i == 2:
                label_text = symbolic_labels[2]  # 2
            elif i == N:
                label_text = symbolic_labels[4]  # N
            elif i == N + 1:
                label_text = symbolic_labels[5]  # N+1
            else:
                label_text = symbolic_labels[3]  # \ldots
                
            label = MathTex(label_text, font_size=24)
            # Position label at the center of the cell
            label.move_to(
                grid.get_corner(DOWN+LEFT) + 
                [(i + 0.5) * cell_size, -0.5 * cell_size, 0]
            )
            labels.add(label)
        
        # Row labels (y-axis)
        for i in range(N + 2):  # 0 to N+1
            # Choose the appropriate label
            if i == 0:
                label_text = symbolic_labels[0]  # 0
            elif i == 1:
                label_text = symbolic_labels[1]  # 1
            elif i == 2:
                label_text = symbolic_labels[2]  # 2
            elif i == N:
                label_text = symbolic_labels[4]  # N
            elif i == N + 1:
                label_text = symbolic_labels[5]  # N+1
            else:
                label_text = symbolic_labels[3]  # \ldots
                
            label = MathTex(label_text, font_size=24)
            # Position label at the center of the cell
            label.move_to(
                grid.get_corner(DOWN+LEFT) + 
                [-0.5 * cell_size, (i + 0.5) * cell_size, 0]
            )
            labels.add(label)
        
        # Create a text explanation area on the right
        explanation_area = Rectangle(
            width=4,
            height=4,
            stroke_width=0,
            fill_opacity=0
        ).move_to(RIGHT * 3)
        
        # Highlight the boundary cells
        boundary_rects = VGroup()
        
        # Top and bottom rows
        for i in range(N + 2):
            # Bottom row (y=0)
            bottom_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [i * cell_size + cell_size/2, cell_size/2, 0]
            )
            boundary_rects.add(bottom_rect)
            
            # Top row (y=N+1)
            top_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [i * cell_size + cell_size/2, (N+1) * cell_size + cell_size/2, 0]
            )
            boundary_rects.add(top_rect)
        
        # Left and right columns (excluding corners already covered)
        for i in range(1, N + 1):
            # Left column (x=0)
            left_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [cell_size/2, i * cell_size + cell_size/2, 0]
            )
            boundary_rects.add(left_rect)
            
            # Right column (x=N+1)
            right_rect = Rectangle(
                height=cell_size,
                width=cell_size,
                stroke_opacity=0,
                fill_color=LOGO_BLUE,
                fill_opacity=0.3
            ).move_to(
                grid.get_corner(DOWN+LEFT) + 
                [(N+1) * cell_size + cell_size/2, i * cell_size + cell_size/2, 0]
            )
            boundary_rects.add(right_rect)
        
        # Animation
        self.play(Create(grid))
        self.play(Write(labels), run_time=2)
        self.wait(1)
        
        # Show boundary cells
        boundary_label = Text("Boundary Cells", font_size=30).move_to(explanation_area)
        
        self.play(
            FadeIn(boundary_rects),
            Write(boundary_label)
        )
        self.wait(1)
        
        # Show interior cells
        interior_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                interior_rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=LOGO_GREEN,
                    fill_opacity=0.3
                ).move_to(
                    grid.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                interior_rects.add(interior_rect)
        
        interior_label = Text("Interior Cells", font_size=30).move_to(explanation_area)
        
        self.play(FadeOut(boundary_label))
        self.play(
            FadeIn(interior_rects),
            Write(interior_label),
        )
        self.wait(2)

class SimulationStepsAnimation(Scene):
    def construct(self):
        # Parameters
        N = 3  # Smaller grid size for this animation
        cell_size = 0.5
        grid_width = (N + 2) * cell_size
        grid_height = (N + 2) * cell_size
        
        # Function to create a grid
        def create_grid(position, title_text):
            grid_group = VGroup()
            
            # Create the grid lines
            grid = VGroup()
            for i in range(N + 3):  # 0 to N+2 lines
                # Horizontal line
                h_line = Line(
                    start=[-grid_width/2, -grid_height/2 + i * cell_size, 0],
                    end=[grid_width/2, -grid_height/2 + i * cell_size, 0],
                    stroke_width=1.5,
                )
                grid.add(h_line)
                
                # Vertical line
                v_line = Line(
                    start=[-grid_width/2 + i * cell_size, -grid_height/2, 0],
                    end=[-grid_width/2 + i * cell_size, grid_height/2, 0],
                    stroke_width=1.5,
                )
                grid.add(v_line)
            
            # Position grid
            grid.move_to(position)
            grid_group.add(grid)
            
            # Add title
            title = Text(title_text, font_size=24)
            title.next_to(grid, UP, buff=0.3)
            grid_group.add(title)
            
            return grid_group, grid
        
        # Create four grids with titles
        spacing = 3.5  # Horizontal spacing between grids
        
        grid1_group, grid1 = create_grid(LEFT * spacing * 1.5, "Initial Density")
        grid2_group, grid2 = create_grid(LEFT * spacing * 0.5, "Add Forces")
        grid3_group, grid3 = create_grid(RIGHT * spacing * 0.5, "Diffuse")
        grid4_group, grid4 = create_grid(RIGHT * spacing * 1.5, "Move")
        
        # Create arrows between grids
        arrow1 = Arrow(
            start=grid1.get_right() + RIGHT * 0.1,
            end=grid2.get_left() + LEFT * 0.1,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        arrow2 = Arrow(
            start=grid2.get_right() + RIGHT * 0.1,
            end=grid3.get_left() + LEFT * 0.1,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        arrow3 = Arrow(
            start=grid3.get_right() + RIGHT * 0.1,
            end=grid4.get_left() + LEFT * 0.1,
            buff=0.1,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Create elbow arrow that loops back from Move to Initial Density
        midpoint_arrow1 = arrow1.get_center()
        
        # Create points for the elbow path
        elbow_start = grid4.get_right() + RIGHT * 0.1
        elbow_point1 = np.array([elbow_start[0] + 0.5, elbow_start[1], 0])  # Right
        elbow_point2 = np.array([elbow_point1[0], midpoint_arrow1[1] - 1.5, 0])  # Down
        elbow_point3 = np.array([midpoint_arrow1[0], elbow_point2[1], 0])  # Left
        elbow_end = np.array([midpoint_arrow1[0], midpoint_arrow1[1] - 0.1, 0])  # Up to arrow1
        
        # Create the elbow path
        elbow_path = VGroup()
        elbow_path.add(Line(elbow_start, elbow_point1))
        elbow_path.add(Line(elbow_point1, elbow_point2))
        elbow_path.add(Line(elbow_point2, elbow_point3))
        elbow_path.add(Line(elbow_point3, elbow_end))
        
        # Add arrowhead to the end of the elbow
        elbow_arrow = Arrow(
            start=elbow_path[-1].get_start(),
            end=elbow_path[-1].get_end(),
            buff=0,
            max_tip_length_to_length_ratio=0.15
        )
        
        # Group the elbow path with the arrowhead
        elbow_loop = VGroup(elbow_path, elbow_arrow)
        
        # Create sample data for visualization in grids
        
        # Initial density - random pattern
        density_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                opacity = np.random.uniform(0.1, 0.5) if np.random.random() > 0.7 else 0
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid1.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                density_rects.add(rect)
        
        # Add forces - stronger density in center
        forces_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Calculate distance from center
                center_i, center_j = (N + 1) / 2, (N + 1) / 2
                dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)
                max_dist = np.sqrt(2) * N / 2
                
                # Higher opacity in center
                opacity = max(0, 0.8 - dist / max_dist)
                if i == center_i and j == center_j:
                    opacity = 0.9  # Peak at center
                
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid2.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                forces_rects.add(rect)
        
        # Diffuse - smoother transition
        diffuse_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Calculate distance from center with smoother falloff
                center_i, center_j = (N + 1) / 2, (N + 1) / 2
                dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)
                max_dist = np.sqrt(2) * N / 2
                
                # Smoother gradient
                opacity = max(0, 0.7 - (dist / max_dist) * 0.7)
                
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid3.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                diffuse_rects.add(rect)
        
        # Move - shift pattern to simulate advection
        move_rects = VGroup()
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Calculate distance from shifted center to simulate movement
                # Shift to upper right
                shift_i, shift_j = 0.5, 0.5
                center_i, center_j = (N + 1) / 2 + shift_i, (N + 1) / 2 + shift_j
                dist = np.sqrt((i - center_i)**2 + (j - center_j)**2)
                max_dist = np.sqrt(2) * N / 2
                
                # Smoother gradient with shift
                opacity = max(0, 0.7 - (dist / max_dist) * 0.7)
                
                rect = Rectangle(
                    height=cell_size,
                    width=cell_size,
                    stroke_opacity=0,
                    fill_color=RED,
                    fill_opacity=opacity
                ).move_to(
                    grid4.get_corner(DOWN+LEFT) + 
                    [i * cell_size + cell_size/2, j * cell_size + cell_size/2, 0]
                )
                move_rects.add(rect)
        
        # Animation sequence
        # Show grids and titles first
        self.play(
            Create(grid1_group),
            Create(grid2_group),
            Create(grid3_group),
            Create(grid4_group),
        )
        self.wait(0.5)
        
        # Show arrows
        self.play(
            Create(arrow1),
            Create(arrow2),
            Create(arrow3),
        )
        self.wait(0.5)
        
        # Show the data in each grid sequentially
        self.play(FadeIn(density_rects))
        self.wait(0.5)
        
        self.play(FadeIn(forces_rects))
        self.wait(0.5)
        
        self.play(FadeIn(diffuse_rects))
        self.wait(0.5)
        
        self.play(FadeIn(move_rects))
        self.wait(1)
        
        # Show the loop back arrow
        self.play(Create(elbow_path), Create(elbow_arrow))
        self.wait(1)
        
        # Add text to explain the loop
        loop_text = Text("Repeat each timestep", font_size=20)
        # Position the text below the horizontal section of the elbow arrow
        text_position = (elbow_point2 + elbow_point3) / 2  # Middle of the bottom horizontal line
        text_position += DOWN * 0.3  # Move down a bit from the line
        loop_text.move_to(text_position)
        self.play(Write(loop_text))
        self.wait(2)

class CellNeighborsAnimation(Scene):
    def construct(self):
        # Parameters
        cell_size = 1.5
        stroke_width = 3
        arrow_offset = 0.15  # Offset for separating opposing arrows
        
        # Create center cell (i,j)
        center_cell = Square(
            side_length=cell_size,
            stroke_width=stroke_width
        ).move_to(ORIGIN)
        
        # Create neighboring cells
        top_cell = Square(
            side_length=cell_size,
            stroke_width=stroke_width
        ).next_to(center_cell, UP, buff=0)
        
        bottom_cell = Square(
            side_length=cell_size,
            stroke_width=stroke_width
        ).next_to(center_cell, DOWN, buff=0)
        
        left_cell = Square(
            side_length=cell_size,
            stroke_width=stroke_width
        ).next_to(center_cell, LEFT, buff=0)
        
        right_cell = Square(
            side_length=cell_size,
            stroke_width=stroke_width
        ).next_to(center_cell, RIGHT, buff=0)
        
        # Group all cells
        cells = VGroup(center_cell, top_cell, bottom_cell, left_cell, right_cell)
        
        # Create arrows with offsets to prevent overlap
        # Horizontal arrows (left <-> center)
        left_to_center = Arrow(
            start=left_cell.get_right() + LEFT * 0.4 + UP * arrow_offset,
            end=center_cell.get_left() + RIGHT * 0.4 + UP * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        center_to_left = Arrow(
            start=center_cell.get_left() + RIGHT * 0.4 + DOWN * arrow_offset,
            end=left_cell.get_right() + LEFT * 0.4 + DOWN * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        # Horizontal arrows (center <-> right)
        center_to_right = Arrow(
            start=center_cell.get_right() + LEFT * 0.4 + UP * arrow_offset,
            end=right_cell.get_left() + RIGHT * 0.4 + UP * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        right_to_center = Arrow(
            start=right_cell.get_left() + RIGHT * 0.4 + DOWN * arrow_offset,
            end=center_cell.get_right() + LEFT * 0.4 + DOWN * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        # Vertical arrows (top <-> center)
        top_to_center = Arrow(
            start=top_cell.get_bottom() + UP * 0.4 + RIGHT * arrow_offset,
            end=center_cell.get_top() + DOWN * 0.4 + RIGHT * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        center_to_top = Arrow(
            start=center_cell.get_top() + DOWN * 0.4 + LEFT * arrow_offset,
            end=top_cell.get_bottom() + UP * 0.4 + LEFT * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        # Vertical arrows (center <-> bottom)
        center_to_bottom = Arrow(
            start=center_cell.get_bottom() + UP * 0.4 + RIGHT * arrow_offset,
            end=bottom_cell.get_top() + DOWN * 0.4 + RIGHT * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        bottom_to_center = Arrow(
            start=bottom_cell.get_top() + DOWN * 0.4 + LEFT * arrow_offset,
            end=center_cell.get_bottom() + UP * 0.4 + LEFT * arrow_offset,
            buff=0,
            stroke_width=2,
            max_tip_length_to_length_ratio=0.2
        )
        
        # Group all arrows
        arrows = VGroup(
            left_to_center, center_to_left,
            center_to_right, right_to_center,
            top_to_center, center_to_top,
            center_to_bottom, bottom_to_center
        )
        
        # Group cells and arrows together for moving
        cell_diagram = VGroup(cells, arrows)
        
        # Show cells with cross pattern
        self.play(
            Create(center_cell),
            Create(top_cell),
            Create(bottom_cell),
            Create(left_cell),
            Create(right_cell),
        )
        self.wait(0.5)
        
        # Show arrows in pairs
        self.play(
            Create(left_to_center),
            Create(center_to_left),
        )
        self.wait(0.3)
        
        self.play(
            Create(center_to_right),
            Create(right_to_center),
        )
        self.wait(0.3)
        
        self.play(
            Create(top_to_center),
            Create(center_to_top),
        )
        self.wait(0.3)
        
        self.play(
            Create(center_to_bottom),
            Create(bottom_to_center),
        )
        self.wait(1)
        
        # Move the entire diagram to the left
        self.play(
            cell_diagram.animate.shift(LEFT * 3.5)
        )
        self.wait(0.5)
        
        
        diffusion_eq = MathTex(
            r"x'_{i,j} = x_{i,j} + a (x_{i-1,j} + x_{i+1,j} \\ + x_{i,j-1} + x_{i,j+1} - 4 \cdot x_{i,j})",
            font_size=36
        ).move_to(RIGHT * 3 + UP * 1.5)

        diffusion_eq_2 = MathTex(
            r"x_{i,j} = x'_{i,j} - a (x'_{i-1,j} + x'_{i+1,j} \\ + x'_{i,j-1} + x'_{i,j+1} - 4 x'_{i,j})",
            font_size=36
        ).move_to(RIGHT * 3)

        diffusion_eq_3 = MathTex(
            r"x'_{i,j} = x_{i,j} + a (x_{i-1,j} + x_{i+1,j} \\ + x_{i,j-1} + x_{i,j+1} - 4 x_{i,j})/(1 + 4 a)",
            font_size=36
        ).move_to(RIGHT * 3)

        self.play(Write(diffusion_eq))
        self.wait(15)

        self.play(Write(diffusion_eq_2))
        self.wait(15)

        self.play(FadeOut(diffusion_eq), diffusion_eq_2.animate.shift(UP * 1.5))
        self.wait(0.3)

        self.play(Write(diffusion_eq_3))
        self.wait(2)

        # final pause
        self.wait(1)

class VelocityFieldAnimation(Scene):
    def construct(self):
        # Parameters
        n_rows, n_cols = 7, 7  # Grid dimensions
        grid_width, grid_height = 6, 6  # Grid size on screen
        cell_width = grid_width / n_cols
        cell_height = grid_height / n_rows
        
        # Set random seed for reproducibility with slight variation
        np.random.seed(43)  # Changed seed for different randomness
        
        # PART 1: VELOCITY FIELD VISUALIZATION
        # Create grid
        grid = VGroup()
        for i in range(n_rows + 1):
            # Horizontal lines
            h_line = Line(
                start=[-grid_width/2, -grid_height/2 + i * cell_height, 0],
                end=[grid_width/2, -grid_height/2 + i * cell_height, 0],
                stroke_width=1,
                color=LIGHT_GRAY
            )
            grid.add(h_line)
            
        for j in range(n_cols + 1):
            # Vertical lines
            v_line = Line(
                start=[-grid_width/2 + j * cell_width, -grid_height/2, 0],
                end=[-grid_width/2 + j * cell_width, grid_height/2, 0],
                stroke_width=1,
                color=LIGHT_GRAY
            )
            grid.add(v_line)
        
        # Create velocity field (swirling pattern)
        arrows = VGroup()
        
        # Function to calculate velocity at any point
        def get_velocity(x, y):
            # Center of the swirl
            center_x, center_y = 0, 0
            
            # Distance from center
            dx = x - center_x
            dy = y - center_y
            distance = np.sqrt(dx**2 + dy**2)
            
            # Swirl strength decreases with distance from center
            strength = 1.0 - min(1.0, distance / 3.0)
            
            # Tangential velocity (perpendicular to radius)
            vx = -dy * strength
            vy = dx * strength
            
            # Add some randomness
            vx += np.random.uniform(-0.2, 0.2)
            vy += np.random.uniform(-0.2, 0.2)
            
            # Normalize and scale - increased scaling factor
            magnitude = np.sqrt(vx**2 + vy**2)
            if magnitude > 0:
                vx = vx / magnitude * cell_width * 1.2 * strength 
                vy = vy / magnitude * cell_height * 1.2 * strength 
            
            return vx, vy
        
        # Create arrows for each cell
        for i in range(n_rows):
            for j in range(n_cols):
                # Cell center
                x = -grid_width/2 + (j + 0.5) * cell_width
                y = -grid_height/2 + (i + 0.5) * cell_height
                
                # Get velocity at this point
                vx, vy = get_velocity(x, y)
                
                # Create arrow - increased stroke width and tip size
                arrow = Arrow(
                    start=[x, y, 0],
                    end=[x + vx, y + vy, 0],
                    buff=0,
                    stroke_width=3,
                    color=LOGO_BLUE,
                    max_tip_length_to_length_ratio=0.4,
                    max_stroke_width_to_length_ratio=6 
                )
                arrows.add(arrow)
        
        # Animation for velocity field
        self.play(Create(grid))
        self.wait(0.5)
        
        # Show arrows with slight delay for visual interest
        for arrow in arrows:
            self.play(Create(arrow), run_time=0.05)
        
        # Pause to show the velocity field
        self.wait(10)
        
        # PART 2: TRANSITION TO PATH TRACE
        # Fade out the velocity arrows
        self.play(FadeOut(arrows))
        self.wait(0.5)
        
        # PART 3: PATH TRACE VISUALIZATION
        # Create the paths for the particles
        paths_right = VGroup()  # Paths flowing right
        paths_left = VGroup()   # Paths flowing left
        
        # Function to add small random perturbation to point
        def add_perturbation(point, scale=0.2):
            # Add a tiny random perturbation in x and y
            dx = np.random.uniform(-scale, scale) * cell_width
            dy = np.random.uniform(-scale, scale) * cell_height
            return [point[0] + dx, point[1] + dy, point[2]]
        
        # Define a common connection point for path1 and path1b
        connection_point = [-grid_width/2 + 3.5*cell_width, -grid_height/2 + 3.5*cell_height, 0]
        
        # Define path1 (top curve flowing right)
        path1_start = connection_point  # This is the common point
        path1_end = add_perturbation([-grid_width/2 + 6.2*cell_width, -grid_height/2 + 4.1*cell_height, 0])
        
        # Define tangent vector at the connection point (for path1 - right direction)
        path1_tangent = np.array([1.0*cell_width, 0.5*cell_height, 0])
        
        # Use Bezier instead of CubicBezier with correct parameters
        path1 = CubicBezier(
            start_anchor=path1_start,
            end_anchor=path1_end,
            start_handle=path1_start + path1_tangent,
            end_handle=add_perturbation(np.array([-grid_width/2 + 5*cell_width, -grid_height/2 + 4.5*cell_height, 0]))
        )
        path1.set_stroke(RED, width=2.5)
        paths_right.add(path1)
        
        # Define path 1b (top curve flowing left - opposite direction)
        path1b_start = connection_point  # Same connection point
        path1b_end = add_perturbation([-grid_width/2 + 1*cell_width, -grid_height/2 + 4*cell_height, 0])
        
        # Use negative of the same tangent vector at connection point for smooth transition
        path1b_tangent = -path1_tangent
        
        path1b = CubicBezier(
            start_anchor=path1b_start,
            end_anchor=path1b_end,
            start_handle=path1b_start + path1b_tangent,  # Use opposite direction tangent for smoothness
            end_handle=add_perturbation(np.array([-grid_width/2 + 1.8*cell_width, -grid_height/2 + 3.8*cell_height, 0]))
        )
        path1b.set_stroke(LOGO_BLUE, width=2.5)
        paths_left.add(path1b)
        
        # Define path 2 (middle curve flowing right)
        path2_start = [-grid_width/2 + 3.5*cell_width, -grid_height/2 + 2.5*cell_height, 0]
        path2_end = add_perturbation([-grid_width/2 + 6*cell_width, -grid_height/2 + 2.5*cell_height, 0])
        
        path2 = CubicBezier(
            start_anchor=path2_start,
            end_anchor=path2_end,
            start_handle=path2_start + np.array([1*cell_width, 0.2*cell_height, 0]),
            end_handle=add_perturbation(np.array([-grid_width/2 + 5*cell_width, -grid_height/2 + 2.8*cell_height, 0]))
        )
        path2.set_stroke(RED, width=2.5)
        paths_right.add(path2)
        
        # Define path 2b (middle curve flowing left - opposite direction)
        path2b_start = path2_start.copy()  # Same starting point
        path2b_end = add_perturbation([-grid_width/2 + 1*cell_width, -grid_height/2 + 2.5*cell_height, 0])
        
        path2b = CubicBezier(
            start_anchor=path2b_start,
            end_anchor=path2b_end,
            start_handle=path2b_start + np.array([-1.5*cell_width, -0.4*cell_height, 0]),  # Different curvature
            end_handle=add_perturbation(np.array([-grid_width/2 + 2.2*cell_width, -grid_height/2 + 2.2*cell_height, 0]))
        )
        path2b.set_stroke(LOGO_BLUE, width=2.5)
        paths_left.add(path2b)
        
        # Define path 3 (bottom curve flowing right)
        path3_start = [-grid_width/2 + 3.5*cell_width, -grid_height/2 + 1.5*cell_height, 0]
        path3_end = add_perturbation([-grid_width/2 + 6*cell_width, -grid_height/2 + 1.2*cell_height, 0])
        
        path3 = CubicBezier(
            start_anchor=path3_start,
            end_anchor=path3_end,
            start_handle=path3_start + np.array([1*cell_width, -0.2*cell_height, 0]),
            end_handle=add_perturbation(np.array([-grid_width/2 + 5*cell_width, -grid_height/2 + 1*cell_height, 0]))
        )
        path3.set_stroke(RED, width=2.5)
        paths_right.add(path3)
        
        # Define path 3b (bottom curve flowing left - opposite direction)
        path3b_start = path3_start.copy()  # Same starting point
        path3b_end = add_perturbation([-grid_width/2 + 1*cell_width, -grid_height/2 + 1.2*cell_height, 0])
        
        path3b = CubicBezier(
            start_anchor=path3b_start,
            end_anchor=path3b_end,
            start_handle=path3b_start + np.array([-1.2*cell_width, 0.7*cell_height, 0]),  # Different curvature
            end_handle=add_perturbation(np.array([-grid_width/2 + 1.8*cell_width, -grid_height/2 + 1.7*cell_height, 0]))
        )
        path3b.set_stroke(LOGO_BLUE, width=2.5)
        paths_left.add(path3b)
        
        # Combine all paths for reference (right paths first, then left paths)
        paths = VGroup()
        paths.add(*paths_right)
        paths.add(*paths_left)
        
        # Create arrows for start and end points of paths
        path_markers_right = VGroup()
        path_markers_left = VGroup()
        
        # Function to create a small square marker
        def create_marker(position, color=RED):
            marker = Square(side_length=0.1, color=color, fill_opacity=1)
            marker.move_to(position)
            return marker
        
        # Function to calculate tangent at a point on the Bezier curve
        def get_tangent_direction(bezier, t):
            # Get two very close points on the curve and find the direction
            p1 = bezier.point_from_proportion(max(0, t - 0.01))
            p2 = bezier.point_from_proportion(min(1, t + 0.01))
            direction = p2 - p1
            # Normalize the direction vector
            length = np.linalg.norm(direction)
            if length > 0:
                direction = direction / length
            return direction
        
        # Add start markers and arrowheads for right-flowing paths
        for path in paths_right:
            # Start marker
            start_marker = create_marker(path.get_start(), RED)
            path_markers_right.add(start_marker)
            
            # Create arrowhead on the curve
            arrow_length = 0.25
            t = 0.7  # Position along the path
            point = path.point_from_proportion(t)
            direction = get_tangent_direction(path, t)
            arrow = Arrow(
                start=point - direction * arrow_length/2,
                end=point + direction * arrow_length/2,
                buff=0,
                stroke_width=2.5,
                color=RED,
                max_tip_length_to_length_ratio=0.5
            )
            path_markers_right.add(arrow)
            
            # End marker
            end_marker = create_marker(path.get_end(), RED)
            path_markers_right.add(end_marker)
        
        # Add start markers and arrowheads for left-flowing paths
        for path in paths_left:
            # Start marker
            start_marker = create_marker(path.get_start(), LOGO_BLUE)
            path_markers_left.add(start_marker)
            
            # Create arrowhead on the curve
            arrow_length = 0.25
            t = 0.7  # Position along the path
            point = path.point_from_proportion(t)
            direction = get_tangent_direction(path, t)
            arrow = Arrow(
                start=point - direction * arrow_length/2,
                end=point + direction * arrow_length/2,
                buff=0,
                stroke_width=2.5,
                color=LOGO_BLUE,
                max_tip_length_to_length_ratio=0.5
            )
            path_markers_left.add(arrow)
            
            # End marker
            end_marker = create_marker(path.get_end(), LOGO_BLUE)
            path_markers_left.add(end_marker)
        
        # Combine all markers
        path_markers = VGroup()
        path_markers.add(*path_markers_right)
        path_markers.add(*path_markers_left)
        
        # Animation for path trace
        # First, show starting points for right-flowing paths
        start_markers_right = VGroup()
        for i in range(len(paths_right)):
            start_markers_right.add(path_markers_right[i*3])
        
        self.play(FadeIn(start_markers_right))
        self.wait(0.5)
        
        # Draw the right-flowing paths with their arrows and end markers
        for i in range(len(paths_right)):
            path = paths_right[i]
            path_arrow = path_markers_right[i*3 + 1]  # Arrow on the path
            end_marker = path_markers_right[i*3 + 2]  # End marker
            
            self.play(
                Create(path),
                run_time=1
            )
            self.play(
                FadeIn(path_arrow),
                FadeIn(end_marker),
                run_time=0.5
            )
            self.wait(0.3)
        
        self.wait(1)  # Pause before showing left-flowing paths
        
        # Show starting points for left-flowing paths (same as right-flowing ones)
        # These are already shown above, so we don't need to show them again
        
        # Draw the left-flowing paths with their arrows and end markers
        for i in range(len(paths_left)):
            path = paths_left[i]
            path_arrow = path_markers_left[i*3 + 1]  # Arrow on the path
            end_marker = path_markers_left[i*3 + 2]  # End marker
            
            self.play(
                Create(path),
                run_time=1
            )
            self.play(
                FadeIn(path_arrow),
                FadeIn(end_marker),
                run_time=0.5
            )
            self.wait(0.3)

class HodgeDecompositionAnimation(Scene):
    def construct(self):
        # Parameters
        n_rows, n_cols = 10, 10  # Using finer grid for better detail
        grid_width, grid_height = 3.5, 3.5  # Further reduced grid size to create more space
        cell_width = grid_width / n_cols
        cell_height = grid_height / n_rows
        
        # Positions adjusted with more spacing for equation symbols
        left_pos = LEFT * 5    # More spread out horizontally
        center_pos = ORIGIN
        right_pos = RIGHT * 5  # More spread out horizontally
        
        # Equation symbol positions with more space
        equals_pos = LEFT * 2.5
        plus_pos = RIGHT * 2.5
        
        # Function to create a grid
        def create_grid():
            grid_lines = VGroup()
            # Horizontal lines
            for i in range(n_rows + 1):
                h_line = Line(
                    start=[-grid_width/2, -grid_height/2 + i * cell_height, 0],
                    end=[grid_width/2, -grid_height/2 + i * cell_height, 0],
                    stroke_width=1.0,  # Increased stroke width
                    color=WHITE,  # Changed to WHITE for visibility on black background
                    stroke_opacity=0.3  # Reduced opacity for subtlety
                )
                grid_lines.add(h_line)
            
            # Vertical lines
            for j in range(n_cols + 1):
                v_line = Line(
                    start=[-grid_width/2 + j * cell_width, -grid_height/2, 0],
                    end=[-grid_width/2 + j * cell_width, grid_height/2, 0],
                    stroke_width=1.0,  # Increased stroke width
                    color=WHITE,  # Changed to WHITE for visibility on black background
                    stroke_opacity=0.3  # Reduced opacity for subtlety
                )
                grid_lines.add(v_line)
            
            return grid_lines
        
        # Functions for velocity fields
        
        # 1. Combined velocity field (left image)
        def combined_field(x, y):
            # Distance from center
            dx = x
            dy = y
            distance = np.sqrt(dx**2 + dy**2)
            
            # Combine curl and divergence patterns
            
            # Rotational component (curl)
            curl_strength = 1.0 - min(1.0, distance / 2.5)
            vx_curl = -dy * curl_strength
            vy_curl = dx * curl_strength
            
            # Divergence component (gradient)
            div_strength = 1.0 - min(1.0, distance / 2.5)
            vx_div = dx * div_strength
            vy_div = dy * div_strength
            
            # Combine the two fields
            vx = vx_curl * 0.7 + vx_div * 0.3
            vy = vy_curl * 0.7 + vy_div * 0.3
            
            # Add some noise for realism
            vx += np.random.uniform(-0.1, 0.1)
            vy += np.random.uniform(-0.1, 0.1)
            
            # Normalize and scale
            magnitude = np.sqrt(vx**2 + vy**2)
            if magnitude > 0:
                scale_factor = min(1.0, magnitude) * cell_width * 0.85
                vx = vx / magnitude * scale_factor
                vy = vy / magnitude * scale_factor
            
            return vx, vy
        
        # 2. Curl field (divergence-free, middle image)
        def curl_field(x, y):
            # Distance from center
            dx = x
            dy = y
            distance = np.sqrt(dx**2 + dy**2)
            
            # Rotational component (curl)
            curl_strength = 1.0 - min(1.0, distance / 2.5)
            vx = -dy * curl_strength
            vy = dx * curl_strength
            
            # Add some noise for realism
            vx += np.random.uniform(-0.1, 0.1)
            vy += np.random.uniform(-0.1, 0.1)
            
            # Normalize and scale
            magnitude = np.sqrt(vx**2 + vy**2)
            if magnitude > 0:
                scale_factor = min(1.0, magnitude) * cell_width * 0.85
                vx = vx / magnitude * scale_factor
                vy = vy / magnitude * scale_factor
            
            return vx, vy
        
        # 3. Gradient field (right image)
        def gradient_field(x, y):
            # Distance from center
            dx = x
            dy = y
            distance = np.sqrt(dx**2 + dy**2)
            
            # Divergence component (gradient)
            div_strength = 1.0 - min(1.0, distance / 2.5)
            vx = dx * div_strength
            vy = dy * div_strength
            
            # Add some noise for realism
            vx += np.random.uniform(-0.1, 0.1)
            vy += np.random.uniform(-0.1, 0.1)
            
            # Normalize and scale
            magnitude = np.sqrt(vx**2 + vy**2)
            if magnitude > 0:
                scale_factor = min(1.0, magnitude) * cell_width * 0.85
                vx = vx / magnitude * scale_factor
                vy = vy / magnitude * scale_factor
            
            return vx, vy
        
        # Function to create velocity field visualization
        def create_velocity_field(field_function, position):
            arrows = VGroup()
            
            for i in range(n_rows):
                for j in range(n_cols):
                    # Cell center
                    x = -grid_width/2 + (j + 0.5) * cell_width
                    y = -grid_height/2 + (i + 0.5) * cell_height
                    
                    # Get velocity at this point
                    vx, vy = field_function(x, y)
                    
                    # Create arrow
                    arrow = Arrow(
                        start=[x, y, 0],
                        end=[x + vx, y + vy, 0],
                        buff=0,
                        stroke_width=2.0,  # Increased stroke width
                        color=WHITE,  # Changed to WHITE for visibility
                        max_tip_length_to_length_ratio=0.3,
                        max_stroke_width_to_length_ratio=5
                    )
                    arrows.add(arrow)
            
            # Create background for each field to help with visibility
            background = Square(
                side_length=max(grid_width, grid_height),
                fill_color=DARK_GREY,
                fill_opacity=0.2,
                stroke_width=0
            )
            
            field = VGroup(background, create_grid(), arrows)
            field.move_to(position)
            return field
        
        # Create the three velocity field visualizations with the new positions
        combined = create_velocity_field(combined_field, left_pos)
        curl = create_velocity_field(curl_field, center_pos)
        gradient = create_velocity_field(gradient_field, right_pos)
        
        # Create equation symbols with enlarged size and well-positioned
        equals = MathTex("=").scale(2.0).move_to(equals_pos)
        plus = MathTex("+").scale(2.0).move_to(plus_pos)
        
        # Create labels with white text for visibility and positioned for 16:9
        combined_label = Text("Combined Field", font_size=22, color=WHITE).next_to(combined, DOWN, buff=0.3)
        curl_label = Text("Curl Field\n(Divergence-free)", font_size=22, color=WHITE).next_to(curl, DOWN, buff=0.3)
        gradient_label = Text("Gradient Field", font_size=22, color=WHITE).next_to(gradient, DOWN, buff=0.3)
        
        # Create title with more space at top for 16:9 format
        title = Title("Hodge Decomposition of Vector Fields", color=WHITE).shift(UP * 0.3)
        
        # Animation sequence
        self.play(Write(title))
        self.wait(0.5)
        
        # Show the combined field first
        self.play(FadeIn(combined[0]))  # Fade in background
        self.play(Create(combined[1]))  # Draw grid
        self.play(Create(combined[2]))  # Draw arrows
        self.play(Write(combined_label))
        self.wait(1)
        
        # Show equals sign and the curl field
        self.play(Write(equals))
        self.play(FadeIn(curl[0]))  # Fade in background
        self.play(Create(curl[1]))  # Draw grid
        self.play(Create(curl[2]))  # Draw arrows
        self.play(Write(curl_label))
        self.wait(1)
        
        # Show plus sign and the gradient field
        self.play(Write(plus))
        self.play(FadeIn(gradient[0]))  # Fade in background
        self.play(Create(gradient[1]))  # Draw grid
        self.play(Create(gradient[2]))  # Draw arrows
        self.play(Write(gradient_label))
        self.wait(1)
        
        # Final pause to appreciate the decomposition
        self.wait(3)
