"""FROZEN shared horn renderer from the accepted pre-refactor drawing.

Do not change geometry, shading, ridges, random seeds, stroke behaviour or
sampling without the user's explicit permission to unfreeze the horns.
"""
import numpy as np
from matplotlib.path import Path
from matplotlib.collections import PolyCollection
from matplotlib.transforms import Affine2D

# Intentionally separate from the editable palette: horn appearance is frozen.
INK = '#30282d'


def draw(canvas, control, root_radius, seed, pose):
    with canvas.transformed(Affine2D().rotate_deg_around(*pose)):
        _draw_surface(canvas, control, root_radius, seed)


def _draw_surface(canvas, control, root_radius, seed):
    """Curved tapered horn with annular ridges and shaded cross sections.

    The centreline defines growth direction. All ring arcs and fine striae
    are mapped onto its local elliptical cross section, so markings wrap
    the form, compress towards the tip, and never float outside the shell.
    """
    path, line = canvas.path, canvas.line
    head = canvas.transform
    ax = canvas.ax
    c = np.asarray(control,dtype=float)
    rng = np.random.default_rng(seed)
    rings = np.array([.07,.16,.26,.37,.48,.59,.70,.80,.885,.95])

    def frame(t):
        q=1-t
        centre=q**3*c[0]+3*q*q*t*c[1]+3*q*t*t*c[2]+t**3*c[3]
        tangent=3*q*q*(c[1]-c[0])+6*q*t*(c[2]-c[1])+3*t*t*(c[3]-c[2])
        tangent=tangent/np.linalg.norm(tangent)
        normal=np.array([-tangent[1],tangent[0]])
        # Broad rounded root; taper continues to a narrow pointed tip.
        radius=root_radius*(1-t)**.70*(.94+.12*np.sin(np.pi*t))
        # Growth ridges change the contour itself, not just its painted lines.
        swelling=sum(.090*np.exp(-((t-r)/(.024-.012*r))**2) for r in rings)
        radius*=1+swelling
        return centre,tangent,normal,radius

    def surface(t,u):
        centre,tangent,normal,radius=frame(t)
        return centre+normal*radius*u+tangent*radius*.30*np.sqrt(max(0,1-u*u))

    ts=np.linspace(0,1,161)
    outline=[surface(t,-1) for t in ts]+[surface(t,1) for t in ts[::-1]]
    shell=Path(outline+[outline[0]], [Path.MOVETO]+[Path.LINETO]*(len(outline)-1)+[Path.CLOSEPOLY])
    path(shell,'#342a35',INK,21,rough=.6)
    faces,colors=[],[]
    # Smooth muted shading around the curved surface; no metallic white bands.
    tgrid=np.linspace(0,1,125)
    ugrid=np.linspace(-1,1,36)
    for a,b in zip(tgrid[:-1],tgrid[1:]):
        for u,v in zip(ugrid[:-1],ugrid[1:]):
            t=(a+b)/2
            q=(u+v)/2
            _,tangent,normal,_=frame(t)
            z=np.sqrt(max(0,1-q*q))
            normal3=np.array([normal[0]*q,normal[1]*q,z])
            lamp=np.array([-.55,-.8,1.0]); lamp/=np.linalg.norm(lamp)
            illumination=max(0,float(np.dot(normal3,lamp)))
            grooves=sum(np.exp(-((t-(r-.014))/.008)**2) for r in rings)
            ridge=sum(np.exp(-((t-(r+.012))/.012)**2) for r in rings)
            value=.27+.67*illumination-.13*grooves+.055*ridge
            value=np.clip(value,0,1)
            dark=np.array([40,32,42]); light=np.array([109,92,109])
            rgb=(dark+(light-dark)*value)/255
            faces.append([surface(a,u),surface(a,v),surface(b,v),surface(b,u)])
            colors.append(rgb)
    canvas.layer+=1
    mesh=PolyCollection(faces,facecolors=colors,edgecolors=colors,
                        linewidths=.15,antialiaseds=False,
                        transform=head+ax.transData,zorder=canvas.layer)
    mesh.set_clip_path(shell,head+ax.transData)
    ax.add_collection(mesh)
    # Each groove curves away around the horn. Thin near-tip rings are closer.
    for r in rings:
        points=[surface(r,u) for u in np.linspace(-.98,.98,61)]
        line(points,'#322834',4.8*(1-r)+1.2,.83)
        highlight=[surface(min(.997,r+.016),u) for u in np.linspace(-.82,.60,48)]
        line(highlight,'#9e879c',2.5*(1-r)+.7,.43)
        # A broken secondary lip makes the growth bands less mechanically uniform.
        start=float(rng.uniform(-.95,-.65)); stop=float(rng.uniform(.25,.65))
        seam=[surface(max(.005,r-.025),u) for u in np.linspace(start,stop,31)]
        line(seam,'#201d26',1.2+.7*(1-r),.30)
    # Very subtle longitudinal keratin grain; it follows the curved growth axis.
    for u in np.linspace(-.85,.87,12):
        a=float(rng.uniform(.05,.37)); b=float(rng.uniform(.63,.95))
        points=[]
        phase=float(rng.uniform(0,6.28))
        for t in np.linspace(a,b,90):
            wav=u+.008*np.sin(t*29+phase)+.003*np.sin(t*81)
            points.append(surface(t,float(np.clip(wav,-.99,.99))))
        line(points,'#ac91a3' if u<0 else '#1d1b24',float(rng.uniform(.65,1.2)),.075)
    # Restore a clear cartoon contour around the shaded material.
    path(shell,'none',INK,20,rough=.7)
